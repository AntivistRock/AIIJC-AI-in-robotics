from source.engine import IResource
import source.engine.camera as camera

import source.objects as objects

from source.utils import rotate

from pybullet_data import getDataPath
from pybullet_utils.bullet_client import BulletClient

from time import sleep


class IScene(IResource):
    def __init__(self, pb_client: BulletClient) -> None:

        IResource.__init__(self)

        self.pb_client = pb_client

        # objects
        self.plane = objects.Plane(self.pb_client)
        self.robot = objects.Robot(self.pb_client)
        self.table = objects.Table(self.pb_client)
        self.kettle = objects.Kettle(self.pb_client)

        # camera
        self.camera = camera.Camera(
            pixel_width=64,
            pixel_height=64,
            view_matrix_data=camera.ViewMatrixData(
                position=[0, 0, 0],
                angles=[0, 0, 0],
                up_vector=[0, 0, 1],
                orient=[0, 0, 1],
                offset=[0, 0, 0]
            ),
            proj_matrix_data=camera.ProjMatrixData(
                near_plane=0.01,
                far_plane=1,
                fov=60
            )
        )

    def _load(self):
        self.pb_client.resetSimulation()
        # set pybullet settings
        self.pb_client.setAdditionalSearchPath(getDataPath())
        self.pb_client.setGravity(0, 0, -9.8)
        self.pb_client.setRealTimeSimulation(1)
        self.pb_client.setTimeStep(0.1)
        # load objects
        self.plane.load()
        self.robot.load()
        self.table.load()
        self.kettle.load()

    def _upload(self):
        self.robot.upload()
        self.kettle.upload()
        self.table.upload()
        self.plane.upload()

    def update_camera(self) -> None:
        pos, orient = self.robot.get_camera_pos()
        self.camera.view_matrix.data.position = pos
        self.camera.view_matrix.data.orient = orient
        self.camera.view_matrix.update()

    def get_state(self):
        return self.camera.snapshot()

    def get_reward(self) -> int:
        raise NotImplementedError()


class ISceneCreator(object):
    def __init__(self, scene_creator):
        self.scene_creator = scene_creator

    def construct(self, pb_client: BulletClient) -> IScene:
        return self.scene_creator(pb_client)
