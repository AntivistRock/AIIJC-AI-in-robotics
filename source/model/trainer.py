import numpy as np
import torch
from pybullet import GUI
import pandas as pd
import matplotlib.pyplot as plt

import engine
from .history import History

from .i_model import Model


def to_one_hot(y, n_dims=None):
    y_tensor = torch.tensor(y, dtype=torch.int64).reshape(-1, 1).to('cuda')
    n_dims = n_dims if n_dims is not None else int(torch.max(y_tensor)) + 1
    y_one_hot = torch.zeros(y_tensor.size()[0], n_dims).to('cuda').scatter_(1, y_tensor, 1)
    return y_one_hot


class Trainer(object):
    def __init__(self):

        self.model = Model(6)
        self.pool = engine.EnvPool(self.model)

        self.opt = torch.optim.Adam(self.model.agent.parameters(), lr=1e-5)

        self.n_actions = 6
        self.moving_average = lambda x, **kw: pd.DataFrame({'x': np.asarray(x)}).x.ewm(**kw).mean().values
        self.evaluate_history = []

    def evaluate(self, n_actions=10):
        with torch.no_grad():
            eval_pool = engine.EnvPool(self.model, evaluation=True)
            self.model.agent.eval()
            history = eval_pool.interract(1, 7)
            self.evaluate_history.append(sum(history.rewards[0]))
        self.model.agent.train()
        plt.plot(self.evaluate_history, label='rewards')
        plt.plot(self.moving_average(np.array(self.evaluate_history), span=10), label='rewards ewma@10')
        plt.legend()
        plt.show()

    def train_on_rollout(self, history: History, prev_memory_states, gamma=0.99):

        states = torch.tensor(np.array(history.states), dtype=torch.float32)  # [batch_size, time, c, h, w]
        actions = torch.tensor(np.array(history.actions), dtype=torch.int64).to('cuda')  # [batch_size, time]
        rewards = torch.tensor(np.array(history.rewards), dtype=torch.float32).to('cuda')  # [batch_size, time]
        rollout_length = rewards.shape[1] - 1

        memory = [m.detach() for m in prev_memory_states]
        memory = tuple(memory)
        logits = []
        state_values = []
        for t in range(rewards.shape[1]):
            obs_t = states[:, t]

            memory, (logits_t, values_t) = self.model.forward(obs_t, memory)
            logits.append(logits_t)
            state_values.append(values_t)

        logits = torch.stack(logits, dim=1)
        state_values = torch.stack(state_values, dim=1)
        probas = torch.softmax(logits, dim=2)
        logprobas = torch.log_softmax(logits, dim=2)

        # выбираем лог-вероятности для реальных действий -- log pi(a_i|s_i)
        actions_one_hot = to_one_hot(actions, self.n_actions).view(
            actions.shape[0], actions.shape[1], self.n_actions)
        logprobas_for_actions = torch.sum(logprobas * actions_one_hot, dim=-1)

        # 1) Policy gradient
        j_hat = 0  # посчитаем ниже

        # 2) Temporal difference MSE
        value_loss = 0

        cumulative_returns = state_values[:, -1].detach()
        for t in reversed(range(rollout_length)):
            r_t = rewards[:, t]  # текущие reward-ы
            v_t = state_values[:, t]  # value текущих состоияний
            v_next = state_values[:, t + 1].detach()  # value следующих состояний
            logpi_a_s_t = logprobas_for_actions[:, t]  # вероятности сделать нужное действие

            cumulative_returns = r_t + gamma * cumulative_returns

            value_loss += (r_t + gamma * v_next - v_t) ** 2

            advantage = cumulative_returns - v_t
            advantage = advantage.detach()

            j_hat += logpi_a_s_t * advantage

        entropy_reg = torch.mean(logprobas * probas)  # entropy regularizer

        loss = -j_hat.mean() + value_loss.mean() + -0.01 * entropy_reg

        self.opt.zero_grad()

        loss.backward()

        self.opt.step()

    def train(self, n):

        for rollout_number in range(n):
            print(f"Start another rollout training. Number {rollout_number}")
            history = self.pool.interract(5, 7)
            self.train_on_rollout(history, self.model.agent.get_initial_state(5))
            print("Finish another rollout training")
            if rollout_number % 50 == 0:
                print("Evaluating")
                self.evaluate()
                print("Finish evaluating")

            if rollout_number % 15 == 0:
                print("Save weights")
                torch.save(self.model.agent.state_dict(), f"../res/agent_weights/agent_weight_{rollout_number}.pth")
