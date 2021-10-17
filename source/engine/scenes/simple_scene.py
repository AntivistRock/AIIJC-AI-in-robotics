from .i_scene import IScene, ISceneCreator

from pybullet_utils.bullet_client import BulletClient


class SimpleScene(IScene):
    def __init__(self, pb_client: BulletClient):
        IScene.__init__(self, pb_client)

    def _update(self):
        self.robot.move([0.01, 0, 0])
        self.robot.update()
        return True

    def get_reward(self) -> int:
        return 1


class SimpleSceneCreator(ISceneCreator):
    def __init__(self):
        ISceneCreator.__init__(self, SimpleScene)
