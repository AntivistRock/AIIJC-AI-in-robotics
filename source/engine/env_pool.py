from utils import ThreadPool


class EnvPool(ThreadPool):
    def __init__(self, env, games_count):
        super().__init__()
