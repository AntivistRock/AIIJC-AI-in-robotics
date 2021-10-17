from .agent import Agent

from .scenes import IScene, ISceneCreator

from source.model import Model, History
from source.utils import add_timer

import os


class Environment (object):
    @add_timer
    def __init__(self, pb_client, model: Model):

        self.pb_client = pb_client

        self.agent = Agent(model)
        self.scene: IScene

    @add_timer
    def run(self, n_steps, history: History):
        if self.scene:
            print(f"> environment::run \n\tpid: {os.getpid()} \n\tppid: {os.getppid()}")
            self.reset()
            for _ in range(n_steps):
                # update scene
                self.scene.update_camera()
                if not self.scene.update():
                    break
                # move robot
                state = self.scene.get_state()
                action = self.agent.get_action(state)
                self.scene.robot.action(action)
                # write history
                history.add(History.Node(
                    action=action,
                    state=state,
                    reward=self.scene.get_reward()
                ))
        else:
            raise RuntimeWarning("didn't find scene")

    @add_timer
    def reset(self):
        self.scene.upload()
        self.scene.load()

    def set_scene(self, scene_creator: ISceneCreator):
        self.scene = scene_creator.construct(self.pb_client)
