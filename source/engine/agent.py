from .i_resource import IResource
from .simulation import Simulation


class Agent(IResource):
    def __init__(self, model, sim_com):
        IResource.__init__(self)

        self.model = model
        self.sim_com = sim_com

        self.last_action = None

    def _update(self):
        # action = self.model.get_action()
        action = 7

        self.sim_com.action(Simulation.MoveRobot(action))

        self.last_action = action

    def _load(self):
        pass

    def _upload(self):
        pass
