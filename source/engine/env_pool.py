import utils


class EnvPool(utils.ThreadPool):
    def __init__(self, env, games_count):
        super().__init__(lambda: 0)
