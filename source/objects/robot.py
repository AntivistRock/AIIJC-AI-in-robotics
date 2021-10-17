import source.engine as engine
import source.utils as utils

import numpy as np
from time import sleep


class Robot(engine.ILoader):

    def _load(self):

        self.pos = np.array([0.4, 0, 0.85])
        self.orient = [0, -np.pi / 2, 0]

        self.arm = self.pb_client.loadURDF(
            r"./source/ext/objects/robot/ur10-wsg50-realsense.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        self.end_effector_link_index = 8
        self.realsense_camera_link_index = 17

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == self.pb_client.JOINT_REVOLUTE] + [9, 10]

        for current_joint_info in self.joint_info:
            print(f"Name: {current_joint_info[1]}; Number: {current_joint_info[0]}; Type {current_joint_info[2]}")



        self.update()

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

        sleep(1)

    def get_realsense_link_state(self):
        state = self.pb_client.getLinkState(self.arm, self.realsense_camera_link_index)
        pos = np.array(state[0])
        angles = np.array(self.pb_client.getEulerFromQuaternion(state[1]))
        return pos, angles

    def action(self, action):
        pass

    def move(self, vec):
        self.pos += utils.rotate(vec, self.orient)

    def grip(self, cmd):
        self.pb_client.setJointMotorControl2(
            self.arm, 11, self.pb_client.VELOCITY_CONTROL, targetVelocity=cmd, force=500)
        self.pb_client.setJointMotorControl2(
            self.arm, 14, self.pb_client.VELOCITY_CONTROL, targetVelocity=-cmd, force=500)

    def rotate(self, angle):
        self.orient[0] += angle
