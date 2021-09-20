import engine
import utils
import numpy as np
import time


class Robot(engine.ILoader):

    def __init__(self, pb_client):
        engine.ILoader.__init__(self)
        self.pb_client = pb_client

    def get_pos(self):
        return self._pos

    def open_gripper(self):
        self.pb_client.setJointMotorControl2(
            self.arm, 9, self.pb_client.VELOCITY_CONTROL, targetVelocity=100, force=10000)
        self.pb_client.setJointMotorControl2(
            self.arm, 10, self.pb_client.VELOCITY_CONTROL, targetVelocity=100, force=10000)
        self.pb_client.stepSimulation()

    def close_gripper(self):
        self.pb_client.setJointMotorControl2(
            self.arm, 9, self.pb_client.VELOCITY_CONTROL, targetVelocity=-100, force=10000)
        self.pb_client.setJointMotorControl2(
            self.arm, 10, self.pb_client.VELOCITY_CONTROL, targetVelocity=-100, force=10000)
        self.pb_client.stepSimulation()

    def rotate_left(self):
        self.rotate(-np.pi / 12)

    def rotate_right(self):
        self.rotate(np.pi / 12)

    def move_forward(self):
        move_vec = np.array([0.1, 0, 0])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def move_back(self):
        move_vec = np.array([-0.1, 0, 0])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def move_right(self):
        move_vec = np.array([0, -0.1, 0])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def move_left(self):
        move_vec = np.array([0, 0.1, 0])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def move_up(self):
        move_vec = np.array([0, 0, 0.1])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def move_down(self):
        move_vec = np.array([0, 0, -0.1])
        self._pos += utils.rotate(move_vec, [0, 0, -self._orient[2]])

    def _load(self):
        self._pos = np.array([0., 0.2, 0.85])
        self._orient = [-np.pi / 2, np.pi / 2, np.pi / 2]

        self.arm = self.pb_client.loadURDF(
            r"./ext/objects/ur10_robot/dependencies/ur_description/urdf/ur10_robot_with_graper.urdf",
            basePosition=[0, 0, 0], useFixedBase=True)

        self.end_effector_link_index = self.pb_client.getNumJoints(self.arm) - 2

        self.joint_info = [self.pb_client.getJointInfo(self.arm, i)
                           for i in range(self.pb_client.getNumJoints(self.arm))]
        self.joint_indices = [x[0] for x in self.joint_info if x[2] == self.pb_client.JOINT_REVOLUTE] + [9, 10]

        self.move()

        time.sleep(1)

    def rotate(self, angle):
        self._orient[0] += angle

    def move(self):
        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.arm, self.end_effector_link_index,
            self._pos, self.pb_client.getQuaternionFromEuler(self._orient)
        )

        self.pb_client.setJointMotorControlArray(
            self.arm, self.joint_indices,
            self.pb_client.POSITION_CONTROL,
            targetPositions=arm_target_pos
        )
