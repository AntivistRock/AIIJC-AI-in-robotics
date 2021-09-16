class History(object):
    class Node(object):
        def __init__(self, action, reward):
            self.action = action
            self.reward = reward

    def __init__(self):
        self.memory = list()

    def add(self, node: Node):
        self.memory.append(node)
