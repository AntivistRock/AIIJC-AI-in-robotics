from .agent import Agent
from .simulation import Simulation

import model

import pybullet as pb
from pybullet_utils import bullet_client


class Environment (object):

    def __init__(self, i_model, connection_mode=pb.DIRECT):
        super().__init__()

        self.pb_client = bullet_client.BulletClient(connection_mode)

        self.simulation = Simulation(self.pb_client)
        self.sim_com = self.simulation.get_com()

        self.agent = Agent(i_model, self.sim_com)
        self.agent_com = self.agent.get_com()

        self.history = model.History()

    def run(self, max_num_upd):
        self.reset()

        for _ in range(max_num_upd):
            if not self.update():
                break
      
    def update(self):
        is_running = self.simulation.update()
        self.agent.update()

        pred_getter = Agent.GetPrediction()
        self.agent_com.action(pred_getter)

        reward_getter = Simulation.GetReward()
        self.sim_com.action(reward_getter)

        history_object = model.History.Node(
            pred_getter.get(),
            reward_getter.get()
        )

        self.history.add(history_object)

        return is_running

    def reset(self):
        self.simulation.reset()
