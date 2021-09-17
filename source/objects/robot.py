import engine
import utils

import pybullet as pb


class Robot(engine.ILoader):

    def __init__(self, pb_client):
        engine.ILoader.__init__(self)
        self.pb_client = pb_client

    def _load(self):

        self._pos = [0.5, 0.2, 0]

        self.arm = self.pb_client.loadURDF(
            r"..\..\ext\models\manip\dependencies\ur_description\urdf\ur10_robot.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        # self.griper = self.pb_client.loadURDF(
        #     r"..\..\ext\models\schunk_wsg50_model\models\wsg50_110.urdf",
        # )
        #
        # self.pb_client.createConstraint(
        #     self.arm, self.pb_client.getNumJoints(self.arm) - 1,
        #     self.griper, 0, pb.JOINT_FIXED,
        #     [1, 0, 0], [0, 0, 0], [0, 0, 0]
        # )

        self.end_effector_link_index = self.pb_client.getNumJoints(self.arm) - 1

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == pb.JOINT_REVOLUTE]

    def rotate(self, angles):
        self._pos = utils.rotate(self._pos, angles)

    def move(self):
        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.arm, self.end_effector_link_index, self._pos)

        self.pb_client.setJointMotorControlArray(
            self.arm, self.joint_indices,
            pb.POSITION_CONTROL, targetPositions=arm_target_pos
        )
