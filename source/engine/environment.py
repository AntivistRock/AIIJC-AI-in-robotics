from .agent import Agent

from source.model import Model
from source.utils import add_timer

import os


class Environment (object):
    @add_timer
    def __init__(self, pb_client, model: Model):

        self.pb_client = pb_client

        self.agent = Agent(model)
        self.scene = None

    @add_timer
    def run(self, n_steps):
        if self.scene:
            print(f"> environment::run \n\tpid: {os.getpid()} \n\tppid: {os.getppid()}")
            self.reset()
            for _ in range(n_steps):
                # self.scene.update_camera()
                self.scene.update()
                # action = self.agent.update(self.scene.get_image())
                # self.scene.robot.move(action)
                self.pb_client.stepSimulation()
        else:
            raise RuntimeWarning("didn't find scene")

    @add_timer
    def reset(self):
        self.scene.upload()
        self.scene.load()

    def set_scene(self, scene_creator):
        self.scene = scene_creator(self.pb_client)
