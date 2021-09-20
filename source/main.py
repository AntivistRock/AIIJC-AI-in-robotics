import engine
from model.teapot_detectron import TeapotDetectron
from model import Model
import matplotlib.pyplot as plt

from pybullet import GUI


def main():
    env = engine.Environment(Model(6), GUI)
    env.run(1)

    detectron = TeapotDetectron()
    plt.imshow(env.history.states[0].astype("int32"))
    plt.show()
    print("Image shape:", env.history.states[0].reshape((4, 128, 128)).shape)
    image_with_mask = detectron.get_points(env.history.states[0][...,:3].astype("float32"))
    print(image_with_mask.size())


if __name__ == "__main__":
    main()
