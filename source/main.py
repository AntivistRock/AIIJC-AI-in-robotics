import engine
#from model.teapot_detectron import TeapotDetectron
from model import Trainer
import matplotlib.pyplot as plt

from pybullet import GUI


def main():
    trainer = Trainer()
    trainer.train(3)


if __name__ == "__main__":
    main()
