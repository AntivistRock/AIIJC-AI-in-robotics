from .resource import Resource

import pybullet as pb


class Simulation (Resource):

    def reset(self):
        pb.resetSimulation()
        self.load()

    def _upload(self):
        pass


class EmptySimulation (Simulation):

    def _load(self):
        pass

    def _update(self):
        pass
