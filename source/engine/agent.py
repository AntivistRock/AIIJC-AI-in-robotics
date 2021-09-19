from .i_resource import IResource
from .simulation import Simulation


class Agent(IResource):
    def __init__(self, model, sim_com):
        IResource.__init__(self)

        self.model = model
        self.sim_com = sim_com

        self.last_prediction = None

    def _update(self):
        # prediction = self.model.predict()
        prediciton = 2

        self.sim_com.action(Simulation.MoveRobot(prediciton))

        self.last_prediction = prediciton

    def _load(self):
        pass

    def _upload(self):
        pass
