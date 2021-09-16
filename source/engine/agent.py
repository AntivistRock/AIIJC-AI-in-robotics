from .i_resource import IResource
from .simulation import Simulation

import utils


class Agent(IResource, utils.IComutating):
    def __init__(self, model, sim_com):
        IResource.__init__(self)
        utils.IComutating.__init__(self)

        self.model = model
        self.sim_com = sim_com

        self.last_prediction = None

    def _update(self):
        self.last_prediction = self.model.predict()
        self.sim_com.action(Simulation.MoveRobot())

    def _load(self):
        pass

    def _upload(self):
        pass

    class GetPrediction(utils.IGetter):
        def call(self, agent):
            self._value = agent.last_prediction
