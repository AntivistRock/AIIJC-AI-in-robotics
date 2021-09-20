import utils
import model
from .environment import Environment

from copy import deepcopy


class EnvPool(utils.ThreadPool):
    def __init__(self, _model):

        def worker(env, num_steps):
            print(f":> environment: {env}")
            env.run(num_steps)
            print(env.history)
            return env.history

        super().__init__(worker)

        self.model = _model
        self.envs = [Environment(deepcopy(self.model)) for _ in range(self._n_parallel)]

    def interract(self, quantity, num_steps):

        def get_env(i):
            if i < len(self.envs):
                return self.envs[i]

            env = Environment(deepcopy(self.model))
            self.envs.append(env)

            return env

        arguments = [[get_env(i), num_steps] for i in range(quantity)]
        returned_histories = self.run(quantity, arguments)

        main_history = model.History()

        for curr_history in returned_histories:
            main_history.add(model.History.Node(
                curr_history.actions,
                curr_history.states,
                curr_history.rewards
            ))

        print("========== main_history.rewards:", main_history.rewards)

        return main_history
