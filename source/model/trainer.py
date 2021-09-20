import numpy as np
import torch
from pybullet import GUI
import pandas as pd
import matplotlib.pyplot as plt

import engine
from .history import History

from .i_model import Model


def to_one_hot(y, n_dims=None):
    y_tensor = torch.tensor(y, dtype=torch.int64).reshape(-1, 1)
    n_dims = n_dims if n_dims is not None else int(torch.max(y_tensor)) + 1
    y_one_hot = torch.zeros(y_tensor.size()[0], n_dims).scatter_(1, y_tensor, 1)
    return y_one_hot


class Trainer(object):
    def __init__(self):

        self.model = Model(6)
        self.pool = engine.EnvPool(self.model)

        self.opt = torch.optim.Adam(self.model.simple_rec_agent.parameters(), lr=1e-5)

        self.n_actions = 6
        self.moving_average = lambda x, **kw: pd.DataFrame({'x': np.asarray(x)}).x.ewm(**kw).mean().values
        self.evaluate_history = []

    def evaluate(self, n_actions=10):
        """Играет игру от начала до конца и возвращает награды на каждом шаге."""
        with torch.no_grad():
            self.model.simple_rec_agent.eval()
            env = engine.Environment(self.model, GUI)
            self.evaluate_history += sum(env.run(n_actions).rewards)
        self.model.simple_rec_agent.train()
        plt.plot(self.evaluate_history, label='rewards')
        plt.plot(self.moving_average(np.array(self.evaluate_history), span=10), label='rewards ewma@10')
        plt.legend()
        plt.show()

    def train_on_rollout(self, history: History, prev_memory_states, gamma=0.99):
        """
        Берет роллаут -- последовательность состояний, действий и наград, полученных из generate_session.
        Обновляет веса агента через policy gradient.
        Менять параметры Adam-а не рекомендуется.
        """

        # сконвертируем всё в torch.tensor
        states = torch.tensor(np.array(history.states), dtype=torch.float32)  # [batch_size, time, c, h, w]
        actions = torch.tensor(np.array(history.actions), dtype=torch.int64)  # [batch_size, time]
        rewards = torch.tensor(np.array(history.rewards), dtype=torch.float32)  # [batch_size, time]
        rollout_length = rewards.shape[1] - 1

        # теперь нужно посчитать логиты, вероятности и лог-вероятности
        # больше для лосса нам ничего не нужно от модели
        memory = [m.detach() for m in prev_memory_states]
        memory = tuple(memory)
        logits = []
        state_values = []
        for t in range(rewards.shape[1]):
            obs_t = states[:, t]

            # вычислите моделью logits_t и values_t.
            # и зааппендьте их к спискам logits и state_values

            memory, (logits_t, values_t) = self.model.forward(obs_t, memory)
            logits.append(logits_t)
            state_values.append(values_t)

        logits = torch.stack(logits, dim=1)
        state_values = torch.stack(state_values, dim=1)
        probas = torch.softmax(logits, dim=2)
        logprobas = torch.log_softmax(logits, dim=2)
        # print(actions.shape[0], actions.shape[1], n_actions)
        # выбираем лог-вероятности для реальных действий -- log pi(a_i|s_i)
        actions_one_hot = to_one_hot(actions, self.n_actions).view(
            actions.shape[0], actions.shape[1], self.n_actions)
        logprobas_for_actions = torch.sum(logprobas * actions_one_hot, dim=-1)

        # Теперь посчитайте две основные компоненты лосса:
        # 1) Policy gradient
        # Примечание: не забываейте делать .detach() для advantage.
        # Ещё лучше использовать mean, а не sum, чтобы lr не масштабировать.
        # Можно исползовать тут циклы, если хотите.
        j_hat = 0  # посчитаем ниже

        # 2) Temporal difference MSE
        value_loss = 0  # посчитаем ниже

        cumulative_returns = state_values[:, -1].detach()
        for t in reversed(range(rollout_length)):
            r_t = rewards[:, t]  # текущие reward-ы
            v_t = state_values[:, t]  # value текущих состоияний
            v_next = state_values[:, t + 1].detach()  # value следующих состояний
            logpi_a_s_t = logprobas_for_actions[:, t]  # вероятности сделать нужное действие

            # G_t = r_t + gamma * G_{t+1}, как в прошлый раз на reinforce
            cumulative_returns = r_t + gamma * cumulative_returns

            # Посчитайте MSE для V(s)
            value_loss += (r_t + gamma * v_next - v_t) ** 2

            # посчитайте advantage A(s_t, a_t), используя cumulative returns и V(s_t) в качестве бейзлайна
            advantage = cumulative_returns - v_t
            advantage = advantage.detach()

            # посчитаем весь policy loss (-J_hat).
            j_hat += logpi_a_s_t * advantage

        entropy_reg = torch.mean(logprobas * probas)  # compute entropy regularizer

        # усредним всё это дело с какими-то весами
        loss = -j_hat.mean() + value_loss.mean() + -0.01 * entropy_reg
        # print(loss)
        self.opt.zero_grad()

        loss.backward()

        self.opt.step()

    def train(self, n):

        for rollout_number in range(n):

            history = self.pool.run(5, [self.model, 10])
            self.train_on_rollout(history, self.model.get_initial_state(5))

            if rollout_number % 500 == 0:
                self.evaluate()

            if rollout_number % 2000 == 0:
                torch.save(self.model.simple_rec_agent, f"../res/agent_weights/agent_weight_{rollout_number}.pth")
