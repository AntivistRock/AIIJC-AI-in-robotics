import utils
from .environment import Environment


class EnvPool(utils.ThreadPool):
    def __init__(self):

        def worker(model, num_steps):
            env = Environment(model)
            env.run(num_steps)

            return env.history

        super().__init__(worker)

    def interract(self, quantity, arguments):

        histories = self.run(quantity, arguments)

        history = histories[0]

        for curr_history in histories[1:-1]:
            history.concatinate(curr_history)

        return history
