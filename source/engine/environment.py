import pybullet as pb

from .pybullet_client import PyBulletClient
from .res.simulation import Simulation, EmptySimulation


class Environment (object):

    def __init__(self, connection_type=pb.DIRECT, simulation=EmptySimulation()):
        self.pb_client = PyBulletClient(connection_type)
        self.simulation = simulation

    def run(self, max_num_upd=10):
        self.simulation.reset()

        for i in range(max_num_upd):
            if not self.update():
                break

        return self.simulation.get_history()
        
    def update(self):
        pb.stepSimulation()
        return self.simulation.update()

    def reset(self):
        self.simulation.reset()

    def set_simulation(self, simulation: Simulation):
        self.simulation = simulation
