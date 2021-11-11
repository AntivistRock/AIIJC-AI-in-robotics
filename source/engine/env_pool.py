from .environment import Environment
from .bullet_client import BulletClient

from source.model import Model
from source.model import History

from source.utils import add_timer

import pybullet as pb

import multiprocessing as mp


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


def play_env_pool(inp):
    model, env_pool, scene_creator, quantity, n_steps = inp
    return env_pool.play(quantity, n_steps, scene_creator)


class MultiprocessingEnvPool(object):

    def __init__(self, model: Model, n_parallel):

        self.pool = mp.Pool(processes=n_parallel)

        self.model = model
        self.n_parallel = n_parallel

        self.env_pools = [EnvPool(self.model) for i in range(self.n_parallel)]

    def __del__(self):
        self.pool.close()
        self.pool.join()

    def play(self, scene_creator, quantity, n_steps):

        quantity_alone = quantity // self.n_parallel
        inp = [(self.model, self.env_pools[i], scene_creator, quantity_alone, n_steps)
               for i in range(self.n_parallel)]

        for history in self.pool.imap_unordered(play_env_pool, inp):
            print(history)
