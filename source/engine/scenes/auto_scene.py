from .i_scene import IScene, ISceneCreator

from source.utils import is_equal_arrs

from time import sleep


class AutoMoveAndGrepScene(IScene):

    def _load(self):
        IScene._load(self)
        self.is_gripped = False

    def _update(self):
        if not self.is_gripped:
            if is_equal_arrs(self.robot.pos, self.kettle.get_handle_pos(), 0.2):
                self.robot.grip(0.5)
                self.is_gripped = True
            else:
                self.robot.move([0.05, 0, 0])
        else:
            if self.robot.pos[2] < 1.3:
                self.robot.move([0, 0.05, 0])
            else:
                return False

        self.robot.update()

        return True

    def get_reward(self) -> int:
        return 1


class AutoSceneCreator(ISceneCreator):
    def __init__(self):
        ISceneCreator.__init__(self, AutoMoveAndGrepScene)
