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
        self.robot.get_start_pos()

        self.pb_client.setGravity(0, 0, -9.8)

        vm_data = ViewMatrixData(
            [0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0.5, 0]
        )
        pm_data = ProjMatrixData(0.01, 20)

        self.camera = Camera(64, 64, vm_data, pm_data)

        self._last_screen = None

    def _upload(self):
        self.robot.upload()

    def _update(self):
        state = self.pb_client.getLinkState(self.robot.arm, self.robot.end_effector_link_index)

        pos = list(state[0])
        ang = list(self.pb_client.getEulerFromQuaternion(state[1]))

        # pos = rotate(pos, [0.1, 0.1, 0])

        self.camera.update_view_matrix([
            ViewMatrixData.SetCameraPos(pos),
            ViewMatrixData.SetEulerAngles(ang),
        ])

        # self.robot.move(pos)
        self._last_screen = self.camera.snapshot()

        self.pb_client.stepSimulation()
        sleep(1)

        return True

    def get_history(self):
        return [self._last_screen, 0]

    class MoveRobot(utils.ISetter):
        def call(self, sim):
            if self.value == 0:
                pass
            elif self.value == 1:
                sim.robot.rotate([0.1, 0, 0])

            sim.robot.move()
