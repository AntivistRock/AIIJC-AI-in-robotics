import pybullet as pb
from pybullet_utils import bullet_client


class Environment (object):

    def __init__(self, simulation_creator, connection_mode=pb.DIRECT):
        super().__init__()

        self.pb_client = bullet_client.BulletClient(connection_mode)
        self.simulation = simulation_creator(self.pb_client)

    def run(self, max_num_upd):
        self.simulation.reset()

        for _ in range(max_num_upd):
            if not self.update():
                break

        return self.simulation.get_history()
      
    def update(self):
        self.pb_client.stepSimulation()
        return self.simulation.update()

    def reset(self):
        self.simulation.reset()

    def sim_com(self, action):
        self.simulation.com.action(action)

    def set_simulation(self, simulation_creator):
        self.simulation = simulation_creator(self.pb_client)
