import pybullet as pb

from .pybullet_client import PyBulletClient
from .res.simulation import Simulation, EmptySimulation


class Environment (object):

    def __init__(self):
        self.pb_client = PyBulletClient(pb.GUI)
        self.simulation = EmptySimulation()

    def update(self):
        self.simulation.update()
        pb.stepSimulation()

    def reset(self):
        self.simulation.reset()

    def set_simulation(self, simulation: Simulation):
        self.simulation = simulation
        self.simulation.reset()
