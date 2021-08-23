import pybullet as pb

from .pybullet_client import PyBulletClient
from .simulation import Simulation


class Environment (object):

    def __init__(self):
        self.pb_client = PyBulletClient(pb.GUI)

    def step(self):
        pb.stepSimulation()

    def set_simulation(self, simulation: Simulation):
        pb.resetSimulation()
        simulation.load()
