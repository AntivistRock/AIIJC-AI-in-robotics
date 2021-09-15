class Commutator(object):
    class Action(object):
        def call(self, target):
            raise NotImplementedError("Commutator.Action должен обладать предназначением")

    def __init__(self, target):
        self.target = target

    def action(self, action: Action):
        action.call(self.target)


class Comutating(object):
    def __init__(self):
        self.com = Commutator(self)


class Setter(Commutator.Action):
    def __init__(self, value):
        self.value = value
