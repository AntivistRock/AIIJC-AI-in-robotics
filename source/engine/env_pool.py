import utils
from .environment import Environment

from copy import deepcopy


class EnvPool(utils.ThreadPool):
    def __init__(self, model):

        def worker(env, num_steps):
            env.run(num_steps)
            return env.history

        super().__init__(worker)

        self.model = model
        self.envs = [Environment(deepcopy(self.model)) for _ in range(self._n_parallel)]

    def interract(self, quantity, num_steps):

        def get_env(i):
            if i < len(self.envs):
                return self.envs[i]

            env = Environment(deepcopy(self.model))
            self.envs.append(env)

            return env

        arguments = [[get_env(i), num_steps] for i in range(quantity)]
        histories = self.run(quantity, arguments)

        history = histories[0]
        for curr_history in histories[1:-1]:
            history.concatinate(curr_history)

        return history
