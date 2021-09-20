from .i_resource import IResource
from .simulation import Simulation


class Agent(IResource):
    def __init__(self, model, sim_com):
        IResource.__init__(self)

        self.model = model
        self.prev_memory = self.model.agent.get_initial_state(1)

        self.sim_com = sim_com

        self.last_action = None

    def _update(self):

        image_getter = Simulation.GetLastScreen()
        self.sim_com.action(image_getter)

        image = image_getter.get()

        # self.prev_memory, action = self.model.get_action(image, self.prev_memory)
        action = 0

        self.sim_com.action(Simulation.MoveRobot(action))
        self.last_action = action

    def _load(self):
        pass

    def _upload(self):
        pass
