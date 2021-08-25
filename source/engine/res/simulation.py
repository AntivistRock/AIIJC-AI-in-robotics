import pybullet as pb

from .resource import Resource


class Simulation(Resource):

    def reset(self):
        self.upload()

    def get_history(self):
        pass

    def _load(self):
        raise NotImplementedError("Simulation must be implemented method 'Simulation._load()'")

    def _upload(self):
        pb.resetSimulation()

    def _update(self):
        raise NotImplementedError("Simulation must be implemented method 'Simulation._update()'")


class EmptySimulation(Simulation):

    def _load(self):
        pass

    def _update(self):
        pass
