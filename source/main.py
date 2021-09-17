import model
import engine

from pybullet import GUI

from PIL import Image
import numpy as np
from matplotlib import cms


def main():
    agent = model.Model()
    env = engine.Environment(agent)

    env.run(5)

    input()


if __name__ == "__main__":
    main()
