class IMatrix(object):
    def __init__(self):
        self._update()

    def _update(self):
        self._matrix = None

    def get(self):
        return self._matrix
