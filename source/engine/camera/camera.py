import numpy as np
import pybullet as pb

from .proj_matrix import ProjMatrix, ProjMatrixData
from .view_matrix import ViewMatrix, ViewMatrixData


class Camera(object):
    def __init__(self, pixel_width: int, pixel_height: int,
                 view_matrix_data: ViewMatrixData,
                 proj_matrix_data: ProjMatrixData):
        self.screen = (pixel_width, pixel_height)
        self.view_matrix = ViewMatrix(view_matrix_data)
        self.proj_matrix = ProjMatrix(proj_matrix_data, self.screen)

    def snapshot(self):
        img_arr = pb.getCameraImage(
            self.screen[0], self.screen[1],
            self.view_matrix.get(), self.proj_matrix.get(),
            shadow=0, lightDirection=[0, 1, 1], renderer=pb.ER_TINY_RENDERER)

        return np.array(img_arr[4])
