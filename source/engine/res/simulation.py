import pybullet as pb

from .resource import Resource


class Simulation(Resource):

    # TODO: write decorator from NotImplementedError

    def reset(self):
        pb.resetSimulation()
        self.load()

    def _load(self):
        raise NotImplementedError("Simulation object must implement method 'Simulation._load()'")

    def _upload(self):
        pass

    def _update(self):
        raise NotImplementedError("Simulation object must implement method 'Simulation._update()'")


class EmptySimulation(Simulation):

    def _load(self):
        pass

    def _update(self):
        pass
