from source.engine import IResource, settings
import source.engine.camera as camera

import source.objects as objects

from pybullet_data import getDataPath
from pybullet_utils.bullet_client import BulletClient


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
                orient=[-1, 0, 0],
                offset=[0, 0.01, 0]
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
        self.pb_client.setTimeStep(settings.TIME_STEP)
        # load objects
        self.plane.load()
        self.robot.load()
        self.table.load()
        self.kettle.load()

        self.update_camera()

    def _upload(self):
        self.robot.upload()
        self.kettle.upload()
        self.table.upload()
        self.plane.upload()

    def update_camera(self) -> None:
        pos, angles = self.robot.get_realsense_link_state()
        self.camera.view_matrix.data.position = pos
        self.camera.view_matrix.data.angles = angles
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
