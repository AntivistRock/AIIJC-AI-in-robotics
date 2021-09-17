class History(object):
    class Node(object):
        def __init__(self, action, state, reward):
            self.state = state
            self.action = action
            self.reward = reward

    def __init__(self):
        self.states = list()
        self.rewards = list()
        self.actions = list()

        # TODO: rewrite lists to numpy arrays

    def add(self, node: Node):
        self.states.append(node.state)
        self.rewards.append(node.reward)
        self.actions.append(node.action)

    def concatinate(self, other_history):

        # np.append(self.states, other_history.states)
        # np.append(self.actions, other_history.actions)
        # np.append(self.rewards, other_history.rewards)

        other_history = None
