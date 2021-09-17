import utils
from .environment import Environment


class EnvPool(utils.ThreadPool):
    def __init__(self):

        def worker(model, num_steps):
            env = Environment(model)
            env.run(num_steps)

            return env.history

        super().__init__(worker)
