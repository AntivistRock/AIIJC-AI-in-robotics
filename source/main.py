from time import sleep

import numpy as np
import pybullet as pb
import pybullet_data

from matplotlib import pyplot as plt

from source import engine, models


class MySimulation(engine.res.Simulation):
    kettle = models.Kettle()
    robot = models.Robot()

    def _load(self):
        pb.setGravity(0, 0, -9.8)
        pb.setRealTimeSimulation(1)

        self.kettle.load()
        self.robot.load()
        
        pb.setAdditionalSearchPath(pybullet_data.getDataPath())
        pb.loadURDF("plane.urdf")

        vm_data = engine.ViewMatrix.ViewMatrixData([0, 0, 5], 10, 2)
        pm_data = engine.ProjMatrix.ProjMatrixData(0.01, 20)

        self.camera = engine.Camera(200, 200, vm_data, pm_data)

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
        
        plt.imshow(self.camera.snapshot())
        
        sleep(2)

def main():
    env = engine.Environment()
    env.set_simulation(MySimulation())

    while True:
        env.update()


if __name__ == "__main__":
    main()
