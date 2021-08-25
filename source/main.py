from time import sleep

import numpy as np
import pybullet as pb

from source import engine, models


class MySimulation(engine.res.Simulation):
    kettle = models.Kettle()
    robot = models.Robot()

    def _load(self):
        pb.setGravity(0, 0, -9.8)
        pb.setRealTimeSimulation(1)

        self.kettle.load()
        self.robot.load()

    def _upload(self):
        self.kettle.upload()
        self.robot.upload()

    def _update(self):
        ax = np.random.choice([0, 1, 2])
        add = np.random.choice([0.1, 0.2, 0.3, -0.1, -0.2, -0.3])
        pos = list(pb.getLinkState(self.robot.arm, self.robot.end_effector_link_index)[0])
        pos[ax] += add

        target_pos = pb.calculateInverseKinematics(self.robot.arm, self.robot.end_effector_link_index, pos)
        pb.setJointMotorControlArray(self.robot.arm, self.robot.joint_indices, pb.POSITION_CONTROL,
                                     targetPositions=target_pos)
        sleep(2)


def main():
    env = engine.Environment()
    env.set_simulation(MySimulation())

    while True:
        env.update()


if __name__ == "__main__":
    main()
