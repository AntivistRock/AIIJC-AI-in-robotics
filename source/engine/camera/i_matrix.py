class IMatrix(object):
    def __init__(self):
        self._matrix = None
        self.update()

    def update(self):
        raise NotImplementedError()

    def get(self):
        return self._matrix
