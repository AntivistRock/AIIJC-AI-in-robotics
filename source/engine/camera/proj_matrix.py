import pybullet as pb

from source.engine.camera.i_matrix import IMatrix


class ProjMatrixData(object):
    def __init__(self, near_plane: float, far_plane: float, fov=60):
        self.plane = (near_plane, far_plane)
        self.fov = fov


class ProjMatrix(IMatrix):

    def __init__(self, data: ProjMatrixData, screen):
        self.data = data
        self.aspect = screen[0] / screen[1]
        super().__init__()

    def update(self):
        self._matrix = pb.computeProjectionMatrixFOV(
            self.data.fov, self.aspect,
            self.data.plane[0], self.data.plane[1]
        )
