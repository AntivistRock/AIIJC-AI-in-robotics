import pybullet as pb

from time import sleep

import engine
import objects


def main():
    env = engine.Environment(objects.MySimulation, pb.GUI)

    env.simulation.load()

    action = objects.MySimulation.MoveRobot([0, 0, 0.9])
    env.sim_com(action)

    sleep(1)

    env.run(10000)


if __name__ == "__main__":
    main()
