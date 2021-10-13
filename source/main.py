import engine
#from model.teapot_detectron import TeapotDetectron

import warnings
warnings.filterwarnings("ignore")

from model import Trainer, Model
import matplotlib.pyplot as plt

from time import sleep
from pybullet import GUI


def main():

    env = engine.Environment(Model(6), GUI)
    env.run(30)
    sleep(60)

    # trainer = Trainer()
    # trainer.train(1000)


if __name__ == "__main__":
    main()
