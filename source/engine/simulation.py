from pybullet_data import getDataPath
from pybullet_utils.bullet_client import BulletClient

import objects
import utils

from math import sqrt
from time import sleep
import numpy as np

from .camera import Camera
from .i_resource import IResource
from .proj_matrix import ProjMatrixData
from .view_matrix import ViewMatrixData


class Simulation(IResource, utils.IComutating):

    def __init__(self, pb_client: BulletClient):
        IResource.__init__(self)
        utils.IComutating.__init__(self)

        self.pb_client = pb_client
        self.kettle = objects.Kettle(self.pb_client)
        self.robot = objects.Robot(self.pb_client)

    def reset(self):
        self.upload()

    def _load(self):

        self.pb_client.setAdditionalSearchPath(getDataPath())
        self.pb_client.setRealTimeSimulation(1)

        self.plane = self.pb_client.loadURDF("plane.urdf")
        self.robot.load()
        self.table = self.pb_client.loadURDF("table/table.urdf", basePosition=[1.2, 0, 0],
                                             baseOrientation=self.pb_client.getQuaternionFromEuler([0, 0, np.pi / 2]))
        self.kettle.load()

        self.pb_client.setGravity(0, 0, -9.8)

        vm_data = ViewMatrixData(
            [0, 0, 0], [0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 0, 0]
        )
        pm_data = ProjMatrixData(0.01, 10)

        self.camera = Camera(64, 64, vm_data, pm_data)

        self.last_screen = None
        print("Sim loaded")

    def _upload(self):
        self.robot.upload()

    def _update(self):
        state = self.pb_client.getLinkState(self.robot.arm, 8)

        pos = list(state[0])
        ang = list(self.pb_client.getEulerFromQuaternion(state[1]))
        pos_for_camera = [pos[0], pos[1], pos[2] + 0.05]
        self.camera.update_view_matrix([
            ViewMatrixData.SetCameraPos(pos_for_camera),
            ViewMatrixData.SetEulerAngles(ang),
        ])

        # self.robot.move(pos)
        self.last_screen = self.camera.snapshot()
        self.kettle.update()

        self.pb_client.stepSimulation()

        #sleep(1)
        #print("Sim new update.")

        return True

    def get_reward(self):
        def count_distance(pos_robot, pos_handle):
            robot_x = pos_robot[0]
            robot_y = pos_robot[1]
            robot_z = pos_robot[2]
            handle_x = pos_handle[0]
            handle_y = pos_handle[1]
            handle_z = pos_handle[2]

            distance = sqrt((robot_x - handle_x)**2 + (robot_y - handle_y)**2 + (robot_z - handle_z)**2)

            return distance

        reward = 0
        handle = self.kettle.get_handle_pos()
        # print('Prev pos dist', count_distance(self.robot.prev_pos, handle))
        # print('Curr pos dist', count_distance(self.robot._pos, handle))
        if count_distance(self.robot.prev_pos, handle) > count_distance(self.robot._pos, handle):
            reward += 1

        reward += 100 if self.kettle.delta_z > 0 else reward
        return reward

    def get_history(self):
        return [self.last_screen, self.get_reward()]

    class GetLastScreen(utils.IGetter):
        def call(self, sim):
            self._value = sim.last_screen

    class MoveRobot(utils.ISetter):

        def call(self, sim):
            if self.value == 0:
                sim.robot.open_gripper()
            elif self.value == 1:
                sim.robot.close_gripper()
            elif self.value == 2:
                sim.robot.move_forward()
            elif self.value == 3:
                sim.robot.move_back()
            elif self.value == 4:
                sim.robot.move_right()
            elif self.value == 5:
                sim.robot.move_left()

            sim.robot.move()
