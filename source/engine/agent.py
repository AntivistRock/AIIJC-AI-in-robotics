class Agent(object):
    def __init__(self, model):
        self.model = model
        self.prev_memory = self.model.agent.get_initial_state(1)

    def get_action(self, image):
        # self.prev_memory, action = self.model.get_action(image, self.prev_memory)
        return 0  # action
