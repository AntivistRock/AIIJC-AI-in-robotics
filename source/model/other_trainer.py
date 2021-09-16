import numpy as np
import pandas as pd

import torch
from tqdm import trange

import engine


def to_one_hot(y, n_dims=None):
    y_tensor = torch.tensor(y, dtype=torch.int64).reshape(-1, 1)
    n_dims = n_dims if n_dims is not None else int(torch.max(y_tensor)) + 1
    y_one_hot = torch.zeros(y_tensor.size()[0], n_dims).scatter_(1, y_tensor, 1)
    return y_one_hot


class Trainer:
    def __init__(self, agent, n_actions):
        self.agent = agent
        self.n_actions = n_actions
        self.env = engine.Environment()
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=1e-5)
        self.pool = engine.EnvPool(engine.Environment, games_count=10)

    def evaluate(self, n_games=1):
        """Играет игру от начала до конца и возвращает награды на каждом шаге."""

        game_rewards = []
        for _ in range(n_games):
            observation = self.env.reset()
            prev_memories = self.agent.get_initial_state(1)

            total_reward = 0
            while True:
                new_memories, readouts = self.agent.step(prev_memories, observation[None, ...])
                action = self.agent.sample_actions(readouts)

                observation, reward, done, info = self.env.update(action)

                total_reward += reward
                prev_memories = new_memories
                if done:
                    break

            game_rewards.append(total_reward)
        return game_rewards

    def train_on_rollout(self, states, actions, rewards, is_not_done, prev_memory_states, gamma=0.99):
        """
        Берет роллаут -- последовательность состояний, действий и наград, полученных из generate_session.
        Обновляет веса агента через policy gradient.
        Менять параметры Adam-а не рекомендуется.
        """

        # сконвертируем всё в torch.tensor
        states = torch.tensor(np.array(states), dtype=torch.float32)  # [batch_size, time, c, h, w]
        actions = torch.tensor(np.array(actions), dtype=torch.int64)  # [batch_size, time]
        rewards = torch.tensor(np.array(rewards), dtype=torch.float32)  # [batch_size, time]
        is_not_done = torch.tensor(is_not_done.astype('float32'), dtype=torch.float32)  # [batch_size, time]
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

            memory, (logits_t, values_t) = self.agent(memory, obs_t)
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
            cumulative_returns = G_t = r_t + gamma * cumulative_returns

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

    def train(self):
        rewards_history = []
        moving_average = lambda x, **kw: pd.DataFrame({'x': np.asarray(x)}).x.ewm(**kw).mean().values
        for i in trange(15000):

            memory = list(self.pool.prev_memory_states)
            rollout_obs, rollout_actions, rollout_rewards, rollout_mask = self.pool.interact()
            self.train_on_rollout(rollout_obs, rollout_actions, rollout_rewards, rollout_mask, memory)

            # if i % 100 == 0:
            #     rewards_history.append(np.mean(self.evaluate()))
            #     clear_output(True)
            #     plt.plot(rewards_history, label='rewards')
            #     plt.plot(moving_average(np.array(rewards_history), span=10), label='rewards ewma@10')
            #     plt.legend()
            #     plt.show()
