import pybullet as pb

from source.engine.res import Loader


class Robot(Loader):

    def _load(self):
        self.arm = pb.loadURDF(
            r"..\..\ext\models\manip\dependencies\ur_description\urdf\ur10_robot.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        self.end_effector_link_index = pb.getNumJoints(self.arm) - 1

        self.joint_info = [pb.getJointInfo(self.arm, i) for i in range(pb.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == pb.JOINT_REVOLUTE]
