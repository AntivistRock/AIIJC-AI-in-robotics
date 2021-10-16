from source.engine import EnvPool
from source.engine.scenes import AutoMoveAndGrepScene

from source.model import Model


def main():
    model = Model(6)

    env_pool = EnvPool(model)
    env_pool.play(1, 1000, AutoMoveAndGrepScene)


if __name__ == "__main__":
    main()
