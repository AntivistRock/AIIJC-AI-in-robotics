from pybullet_data import getDataPath
from pybullet_utils.bullet_client import BulletClient

import objects
import utils

from .camera import Camera
from .i_resource import IResource
from .proj_matrix import ProjMatrixData
from .view_matrix import ViewMatrixData


class Simulation(IResource, utils.IComutating):

    def __init__(self, pb_client: BulletClient):
        IResource.__init__(self)
        utils.IComutating.__init__(self)

        self.pb_client = pb_client
        self.robot = objects.Robot(self.pb_client)

    def reset(self):
        self.upload()

    def get_history(self):
        pass

    def _load(self):
        # self.pb_client.setGravity(0, 0, -9.8)
        self.pb_client.setAdditionalSearchPath(getDataPath())
        self.pb_client.setRealTimeSimulation(1)

        self.plane = self.pb_client.loadURDF("plane.urdf")
        self.robot.load()

        vm_data = ViewMatrixData(
            [0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0.5, 0]
        )
        pm_data = ProjMatrixData(0.01, 20)

        self.camera = Camera(320, 200, vm_data, pm_data)

    def _upload(self):
        self.robot.upload()
        self.pb_client.resetSimulation()

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
        # self.camera.snapshot()

        self.pb_client.stepSimulation()

        return True

    class MoveRobot(utils.Commutator.IAction):

        def __init__(self):
            utils.Commutator.IAction.__init__(self)

        def call(self, sim):
            sim.robot.rotate([0.1, 0.2, 0.1])
            sim.robot.move()

    class GetReward(utils.IGetter):
        def call(self, sim):
            self._value = 1
