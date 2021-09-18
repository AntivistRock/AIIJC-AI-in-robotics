import engine
import utils
import numpy as np


class Robot(engine.ILoader):

    def __init__(self, pb_client):
        engine.ILoader.__init__(self)
        self.pb_client = pb_client

    def get_pos(self):
        return self._pos

    def _load(self):
        self._pos = [0.5, 0.2, 0]

        self.arm = self.pb_client.loadURDF(
            "../exe/objects/arm/dependencies/ur_description/urdf/ur10_new_from_home_pc.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        self.end_effector_link_index = self.pb_client.getNumJoints(self.arm) - 2

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == self.pb_client.JOINT_REVOLUTE] + [9, 10]

    def get_start_pos(self):
        target_pos = self.pb_client.calculateInverseKinematics(self.arm, self.end_effector_link_index,
                                                               [0, 0.1, 0.7],
                                                               self.pb_client.getQuaternionFromEuler(
                                                                   [-np.pi / 2, np.pi / 2, np.pi / 2]))

        self.pb_client.setJointMotorControlArray(self.arm, self.joint_indices, self.pb_client.POSITION_CONTROL,
                                                 targetPositions=target_pos)

    def rotate(self, angles):
        self._pos = utils.rotate(self._pos, angles)

    def move(self):
        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.arm, self.end_effector_link_index, self._pos)

        self.pb_client.setJointMotorControlArray(
            self.arm, self.joint_indices,
            self.pb_client.POSITION_CONTROL, targetPositions=arm_target_pos
        )
