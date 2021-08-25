from .matrix import ViewMatrix, ProjMatrix

import pybullet as pb
import numpy as np


class Camera(object):
    def __init__(self, pixel_width: int, pixel_height: int,
                 view_matrix_data: ViewMatrix.ViewMatrixData,
                 proj_matrix_data: ProjMatrix.ProjMatrixData):

        self.screen = (pixel_width, pixel_height)
        self.view_matrix = ViewMatrix(view_matrix_data)
        self.proj_matrix = ProjMatrix(proj_matrix_data, self.screen)

    def snapshot(self):
        img_arr = pb.getCameraImage(
            self.screen[0], self.screen[1],
            self.view_matrix.get(), self.proj_matrix.get(),
            shadow=0, lightDirection=[0, 1, 1], renderer=pb.ER_TINY_RENDERER)

        return np.array(img_arr[2]).reshape(self.screen[0], self.screen[1], 4)
