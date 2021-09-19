import numpy as np
from numpy import cos, sin


def rotate(vec: np.array, ang: np.array):
    a, b, c = ang

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

    return np.array(np.matmul(rot, vec))[0]
