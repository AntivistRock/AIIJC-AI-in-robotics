import pybullet as pb

from engine.res import Loader


class Robot(Loader):

    def __init__(self, pb_client):
        Loader.__init__(self)
        self.pb_client = pb_client

    def _load(self):
        self.arm = self.pb_client.loadURDF(
            r"..\..\ext\models\manip\dependencies\ur_description\urdf\ur10_new.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        self.end_effector_link_index = self.pb_client.getNumJoints(self.arm) - 1

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == pb.JOINT_REVOLUTE]

    def move(self, pos):
        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.arm, self.end_effector_link_index, pos)

        self.pb_client.setJointMotorControlArray(
            self.arm, self.joint_indices,
            pb.POSITION_CONTROL, targetPositions=arm_target_pos
        )
