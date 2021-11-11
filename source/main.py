from source.engine import MultiprocessingEnvPool
from source.model import Model

import source.engine.scenes as scenes


def main():
    model = Model(6)

    pool = MultiprocessingEnvPool(model, 5)
    pool.play(scenes.AutoSceneCreator(), quantity=10, n_steps=10)


if __name__ == "__main__":
    main()
