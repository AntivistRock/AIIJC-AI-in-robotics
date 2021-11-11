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

    def __str__(self):
        return f"History\n\tstates: {self.states}\n\trewards: {self.rewards}\n\tactions: {actions}"

    def add(self, node: Node):
        self.states.append(node.state)
        self.rewards.append(node.reward)
        self.actions.append(node.action)
