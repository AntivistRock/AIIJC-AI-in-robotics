import engine
from model.teapot_detectron import TeapotDetectron
from model import Model

from pybullet import GUI


def main():
    env = engine.Environment(Model(6))
    env.run(1)

    detectron = TeapotDetectron()

    image_with_mask = detectron.get_points(env.history.states[0])
    print(image_with_mask.size())


if __name__ == "__main__":
    main()
