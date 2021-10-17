from source.engine import EnvPool
from source.model import Model

import source.engine.scenes as scenes


def main():
    model = Model(6)

    pool = EnvPool(model, True)
    pool.play(1, 100, scenes.AutoSceneCreator())


if __name__ == "__main__":
    main()
