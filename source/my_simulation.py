import numpy as np
import pybullet as pb

import engine
import models


class MySimulation(engine.res.Simulation):

    kettle = models.Kettle()
    robot = models.Robot()

    def _load(self):
        pb.setGravity(0, 0, -9.8)
        pb.setRealTimeSimulation(0)

        # self.kettle.load()
        # self.robot.load()

        self.images = []

        vm_data = engine.ViewMatrixData([0, 0, 0.5], 2, 2, (0, -10, 0))
        pm_data = engine.ProjMatrixData(0.01, 20)

        self.camera = engine.Camera(320, 200, vm_data, pm_data)

    def _upload(self):
        self.kettle.upload()
        self.robot.upload()

    def _update(self):
        # ax = np.random.choice([0, 1, 2])
        # pos = list(pb.getLinkState(self.robot.arm, self.robot.end_effector_link_index)[0])
        # pos[ax] += 0.2
        #
        # target_pos = pb.calculateInverseKinematics(self.robot.arm, self.robot.end_effector_link_index, pos)
        # pb.setJointMotorControlArray(
        #     self.robot.arm, self.robot.joint_indices,
        #     pb.POSITION_CONTROL, targetPositions=target_pos
        # )

        self.images.append(self.camera.snapshot())

        return False

    def get_history(self):
        return self.images
