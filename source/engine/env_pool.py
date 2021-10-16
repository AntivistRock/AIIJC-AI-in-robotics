from .environment import Environment
from .bullet_client import BulletClient

from source.model import Model

from source.utils import add_timer

import pybullet as pb


class EnvPool(object):
    @add_timer
    def __init__(self, model: Model) -> None:
        # self.pb_server = BulletClient(pb.SHARED_MEMORY_SERVER, 1234)
        self.pb_client = BulletClient(pb.GUI)
        self.environment = Environment(self.pb_client, model)

    def __del__(self) -> None:
        del self.pb_client
        # del self.pb_server

    @add_timer
    def play(self, quantity: int, n_steps: int, scene_creator) -> None:
        self.environment.set_scene(scene_creator)
        for _ in range(quantity):
            self.environment.run(n_steps)
