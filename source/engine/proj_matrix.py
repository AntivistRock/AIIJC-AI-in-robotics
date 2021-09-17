import pybullet as pb

from utils import IComutating, ISetter
from .i_matrix import IMatrix


class ProjMatrixData(IComutating):
    def __init__(self, near_plane: float, far_plane: float, fov=60):
        IComutating.__init__(self)

        self.plane = (near_plane, far_plane)
        self.fov = fov

    class SetPlane(ISetter):
        def call(self, data):
            data.plane = self.value

    class SetFov(ISetter):
        def call(self, data):
            data.fov = self.value


class ProjMatrix(IMatrix):

    def __init__(self, data: ProjMatrixData, screen):
        self._data = data
        self.aspect = screen[0] / screen[1]
        super().__init__()

    def _update(self):
        self._matrix = pb.computeProjectionMatrixFOV(
            self._data.fov, self.aspect,
            self._data.plane[0], self._data.plane[1]
        )

    def update_set(self, setters):
        for setter in setters:
            setter.call(self._data)

        self._update()
