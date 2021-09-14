import pybullet as pb

from engine import Environment
from objects import Simulation


def main():
    env = Environment(Simulation, pb.GUI)
    env.run(100000)


if __name__ == "__main__":
    main()
