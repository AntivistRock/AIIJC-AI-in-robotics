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
        self.envs = [Environment(None) for _ in range(self._n_parallel)]

    def interract(self, quantity, num_steps):

        [env.set_model(deepcopy(self.model)) for env in self.envs]
        arguments = [[self.envs[i], num_steps] for i in range(self._n_parallel)]
        histories = self.run(quantity, arguments)

        history = histories[0]
        for curr_history in histories[1:-1]:
            history.concatinate(curr_history)

        return history
