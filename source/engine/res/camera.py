from .view_matrix import ViewMatrix, ViewMatrixData
from .proj_matrix import ProjMatrix, ProjMatrixData

import pybullet as pb
import numpy as np


class Camera(object):
    def __init__(self, pixel_width: int, pixel_height: int,
                 view_matrix_data: ViewMatrixData,
                 proj_matrix_data: ProjMatrixData):

        self._screen = (pixel_width, pixel_height)
        self._view_matrix = ViewMatrix(view_matrix_data)
        self._proj_matrix = ProjMatrix(proj_matrix_data, self._screen)

    def snapshot(self):
        img_arr = pb.getCameraImage(
            self._screen[0], self._screen[1],
            self._view_matrix.get(), self._proj_matrix.get(),
            shadow=0, lightDirection=[0, 1, 1], renderer=pb.ER_TINY_RENDERER)

        return np.array(img_arr[2]).reshape(self._screen[0], self._screen[1], 4)

    def update_view_matrix(self, setters: list):
        self._view_matrix.update_set(setters)

