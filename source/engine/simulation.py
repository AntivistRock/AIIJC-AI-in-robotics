from pybullet_utils.bullet_client import BulletClient

from .resource import Resource
from utils import Comutating


class Simulation(Resource, Comutating):

    def __init__(self, pb_client: BulletClient):

        Resource.__init__(self)
        Comutating.__init__(self)

        self.pb_client = pb_client

    def reset(self):
        self.upload()

    def get_history(self):
        pass

    def _load(self):
        raise NotImplementedError("Simulation must be implemented method 'Simulation._load()'")

    def _upload(self):
        self.pb_client.resetSimulation()

    def _update(self):
        raise NotImplementedError("Simulation must be implemented method 'Simulation._update()'")


class EmptySimulation(Simulation):

    def _load(self):
        pass

    def _update(self):
        pass
