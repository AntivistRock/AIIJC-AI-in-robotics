import source.engine as engine
import source.utils as utils

import numpy as np
from time import sleep

MOVE_SPEED = 0.05


class Robot(engine.ILoader):

    def _load(self):
        self.pos = np.array([0.3, 0, 0.85])
        self.orient = [0, np.pi / 2, 0]

        self.arm = self.pb_client.loadURDF(
            r"./source/ext/objects/ur10_robot/dependencies/ur_description/urdf/ur10_robot_with_graper.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)\

        self.end_effector_link_index = 8

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == self.pb_client.JOINT_REVOLUTE] + [9, 10]

        self.update()
        sleep(0.5)

    def _upload(self):
        pass

    def _update(self):
        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.arm, self.end_effector_link_index,
            self.pos, self.pb_client.getQuaternionFromEuler(self.orient)
        )

        self.pb_client.setJointMotorControlArray(
            self.arm, self.joint_indices,
            self.pb_client.POSITION_CONTROL,
            targetPositions=arm_target_pos
        )

    def move(self, vec):
        self.pos += utils.rotate(vec, self.orient)

    def action(self, action):
        pass

    def move_gripper(self, velocity):
        self.pb_client.setJointMotorControl2(
            self.arm, 9, self.pb_client.VELOCITY_CONTROL, targetVelocity=velocity, force=500)
        self.pb_client.setJointMotorControl2(
            self.arm, 10, self.pb_client.VELOCITY_CONTROL, targetVelocity=velocity, force=500)

    def rotate(self, angle):
        self.orient[0] += angle
