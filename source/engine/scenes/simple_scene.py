from .i_scene import IScene

from pybullet_utils.bullet_client import BulletClient


class SimpleScene(IScene):
    def __init__(self, pb_client: BulletClient):
        IScene.__init__(self, pb_client)

    def _update(self):
        return True
