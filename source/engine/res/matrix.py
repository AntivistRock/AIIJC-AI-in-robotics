import numpy as np
from numpy import cos, sin


class Matrix(object):
    def __init__(self):
        self._update()

    def _update(self):
        self._matrix = None

    def get(self):
        return self._matrix


class Setter(object):
    def __init__(self, value):
        self.value = value

    def call(self, data):
        raise NotImplementedError("Setter должен устанавливать значение")


def rotate(vec: np.array, angles: np.array):

    a, b, c = angles
    a, b, c = -a, -b, -c

    rot = np.matrix([
        [
            cos(a) * cos(c) - cos(b) * sin(a) * sin(c),
            cos(b) * cos(c) * sin(a) + cos(a) * sin(c),
            sin(a) * sin(b),
        ],
        [
            -cos(c) * sin(a) - cos(a) * cos(b) * sin(c),
            cos(a) * cos(b) * cos(c) - sin(a) * sin(c),
            cos(a) * sin(b),
        ],
        [
            sin(b) * sin(c),
            -cos(c) * sin(b),
            cos(b),
        ],
    ])

    return np.array(np.matmul(vec, rot))[0]
