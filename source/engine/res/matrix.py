import pybullet as pb


class Matrix(object):
    def __init__(self):
        self._update()

    def _update(self):
        self._matrix = None

    def get(self):
        return self._matrix


class ViewMatrix(Matrix):
    class ViewMatrixData(object):
        def __init__(self, target_pos, distance, up_axis_index, angles=(0, 0, 0)):
            self.target_pos = target_pos
            self.distance = distance
            self.up_axis_index = up_axis_index
            self.angles = angles

    def __init__(self, data: ViewMatrixData):
        self._data = data
        super().__init__()

    def _update(self):
        self._matrix = pb.computeViewMatrixFromYawPitchRoll(
            self._data.target_pos, self._data.distance,
            self._data.angles[0], self._data.angles[1], self._data.angles[2],
            self._data.up_axis_index
        )


class ProjMatrix(Matrix):
    class ProjMatrixData(object):
        def __init__(self, near_plane: float, far_plane: float, fov=60):
            self.plane = (near_plane, far_plane)
            self.fov = fov

    def __init__(self, data: ProjMatrixData, screen):
        self._data = data
        self.aspect = screen[0] / screen[1]
        super().__init__()

    def _update(self):
        self._matrix = pb.computeProjectionMatrixFOV(
            self._data.fov, self.aspect,
            self._data.plane[0], self._data.plane[1]
        )
