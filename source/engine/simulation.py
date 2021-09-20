from pybullet_data import getDataPath
from pybullet_utils.bullet_client import BulletClient

import objects
import utils

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
        self.table = self.pb_client.loadURDF("table/table.urdf", basePosition=[0, 1.5, 0],
                                             baseOrientation=self.pb_client.getQuaternionFromEuler([0, 0, np.pi / 2]))
        self.kettle.load()
        self.robot.load()

        self.pb_client.setGravity(0, 0, -9.8)

        vm_data = ViewMatrixData(
            [0, 0, 0], [0, 0, 0], [0, 0, 1], [-1, 0, 0], [0, 0, 0]
        )
        pm_data = ProjMatrixData(0.01, 10)

        self.camera = Camera(128, 128, vm_data, pm_data)

        self.last_screen = None
        print("Waiting")
        sleep(20)

    def _upload(self):
        self.robot.upload()

    def _update(self):
        state = self.pb_client.getLinkState(self.robot.arm, self.robot.end_effector_link_index)

        pos = self.robot.get_pos()
        ang = list(self.pb_client.getEulerFromQuaternion(state[1]))
        # ang = [ang[0] + np.pi / 2, ang[1], ang[2]]
        ang[0] += np.pi / 2
        # pos = rotate(pos, [0.1, 0.1, 0])

        self.camera.update_view_matrix([
            ViewMatrixData.SetCameraPos(pos),
            ViewMatrixData.SetEulerAngles(ang),
        ])

        # self.robot.move(pos)
        self.last_screen = self.camera.snapshot()
        self.kettle.update()

        self.pb_client.stepSimulation()
        sleep(1)

        return True

    def get_history(self):
        # calc state, reward
        reward = (100 if self.kettle.delta_z > 0 else 0)
        return [self.last_screen, reward]  # [state, reward]

    class GetLastScreen(utils.IGetter):
        def call(self, sim):
            self._value = sim.last_screen

    class MoveRobot(utils.ISetter):

        def call(self, sim):
            #  update orientation before action
            # print("Orientation first:", sim.robot._orient, '\n')
            # sim.robot._orient = sim.robot.pb_client.getEulerFromQuaternion(sim.robot.pb_client.getLinkState(
            #     sim.robot.arm, sim.robot.end_effector_link_index
            # )[1])
            # print("Orientation second:", sim.robot._orient)
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
