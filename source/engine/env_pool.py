from .environment import Environment
from .bullet_client import BulletClient

from source.model import Model
from source.model import History

from source.utils import add_timer

import pybullet as pb


class EnvPool(object):
    @add_timer
    def __init__(self, model: Model, is_view_gui: bool = False) -> None:

        self.pb_client = None
        self.pb_server = None

        if is_view_gui:
            self.pb_client = BulletClient(pb.GUI)
        else:
            self.pb_server = BulletClient(pb.SHARED_MEMORY_SERVER, 1234)
            self.pb_client = BulletClient(pb.SHARED_MEMORY, 1234)

        self.environment = Environment(self.pb_client, model)

    def __del__(self) -> None:
        if self.pb_client:
            del self.pb_client
        if self.pb_server:
            del self.pb_server

    @add_timer
    def play(self, quantity: int, n_steps: int, scene_creator) -> History:
        self.environment.set_scene(scene_creator)
        history = History()
        for _ in range(quantity):
            self.environment.run(n_steps, history)

        return history
