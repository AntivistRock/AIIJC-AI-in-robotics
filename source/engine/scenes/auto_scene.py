from .i_scene import IScene, ISceneCreator

from source.utils import is_equal_arrs

from time import sleep


class AutoMoveAndGrepScene(IScene):

    def _load(self):
        IScene._load(self)
        self.is_grepped = False

    def next_step(self):
        self.pb_client.stepSimulation()
        sleep(0.8)

    def _update(self):
        if not self.is_grepped:
            if is_equal_arrs(self.robot.pos, self.kettle.get_handle_pos(), 0.2):
                # TODO: grep kettle
                self.is_grepped = True
            else:
                self.robot.move([0.05, 0, 0])
        else:
            if self.robot.pos[2] < 1.2:
                self.robot.move([0, -0.1, 0])
            else:
                return False

        sleep(0.5)
        self.robot.update()

        return True

    def get_reward(self) -> int:
        return 1


class AutoSceneCreator(ISceneCreator):
    def __init__(self):
        ISceneCreator.__init__(self, AutoMoveAndGrepScene)
