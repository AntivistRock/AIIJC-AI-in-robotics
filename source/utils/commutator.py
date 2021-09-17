class Commutator(object):
    class IAction(object):

        # @must_be_implemented(error_msg="Commutator.Action должен обладать предназначением")
        def call(self, target):
            raise NotImplementedError()

    def __init__(self, target):
        self.target = target

    def action(self, action: IAction):
        return action.call(self.target)


class IComutating(object):
    def __init__(self):
        self._com = Commutator(self)

    def get_com(self):
        return self._com


class ISetter(Commutator.IAction):
    def __init__(self, value):
        self.value = value


class IGetter(Commutator.IAction):
    def __init__(self):
        self._value = None

    def get(self):
        return self._value
