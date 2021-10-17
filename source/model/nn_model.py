import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as f

# [batch, channel, w, h] -> [batch, units]
class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)


class SimpleRecurrentAgent(nn.Module):
    def __init__(self, im_channels=1, n_actions=6, reuse=False):
        super().__init__()

        self.conv0 = nn.Conv2d(im_channels, 32, kernel_size=(3, 3), stride=(2, 2))
        self.bn1 = nn.BatchNorm2d(32)
        self.conv1 = nn.Conv2d(32, 32, kernel_size=(3, 3), stride=(2, 2))
        self.bn2 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 8, kernel_size=(3, 3), stride=(2, 2))
        self.bn3 = nn.BatchNorm2d(8)
        self.flatten = Flatten()

        self.hid = nn.Linear(392, 128)
        self.rnn = nn.LSTMCell(128, 128)

        self.logits = nn.Linear(128, n_actions)
        self.state_value = nn.Linear(128, 1)

    def forward(self, prev_memory_state, obs_t):
        """
        Принимает предыдущее состояние (память) и наблюдени,
        возвращает следующее состояние и пару из политики (actor) и оценки состояния (critic)
        """
        x = f.relu(self.conv0(obs_t))
        x = self.bn1(x)

        x = f.relu(self.conv1(x))
        x = self.bn2(x)

        x = f.relu(self.conv2(x))
        x = self.bn3(x)
        x = self.flatten(x)

        latent_obs_vector = self.hid(x)
        new_memory_state = self.rnn(latent_obs_vector, prev_memory_state)
        actions_logits = self.logits(new_memory_state[0])
        state_value = self.state_value(new_memory_state[0])

        return new_memory_state, (actions_logits, state_value)

    def get_initial_state(self, batch_size):
        """Возвращает память агента в начале игры."""
        return torch.zeros((batch_size, 128)), torch.zeros((batch_size, 128))

    def sample_actions(self, agent_outputs):
        """Делает случайное действие, в соответствие с предсказанными вероятностями."""
        logits, state_values = agent_outputs
        probs = torch.softmax(logits, dim=-1)
        return torch.multinomial(probs, 1)[:, 0].data.numpy()

    def step(self, prev_state, obs_t):
        """Подобно forward, но obs_t это не торчевый тензор."""
        obs_t = torch.tensor(np.array(obs_t), dtype=torch.float32)
        (h, c), (l, s) = self.forward(prev_state, obs_t)
        return (h.detach(), c.detach()), (l.detach(), s.detach())
