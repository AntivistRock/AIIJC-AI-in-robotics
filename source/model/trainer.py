import engine


class Trainer(object):
    def __init__(self):
        self.pool = engine.EnvPool()

    def train(self, n):
        for _ in range(n):
            pass
