import pybullet as pb


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
        raise NotImplementedError()


class ViewMatrixData(object):
    def __init__(self, target_pos, distance, up_axis_index, angles=(0, 0, 0)):
        self.target_pos = target_pos
        self.distance = distance
        self.up_axis_index = up_axis_index
        self.angles = angles


class ViewMatrix(Matrix):

    def __init__(self, data: ViewMatrixData):
        self._data = data
        super().__init__()

    def _update(self):
        self._matrix = pb.computeViewMatrixFromYawPitchRoll(
            self._data.target_pos, self._data.distance,
            self._data.angles[0], self._data.angles[1], self._data.angles[2],
            self._data.up_axis_index
        )

    def update_set(self, setters):
        for setter in setters:
            setter.call(self._data)

        self._update()

    class SetTargetPos(Setter):
        def call(self, data: ViewMatrixData):
            data.target_pos = self.value

    class SetDistance(Setter):
        def call(self, data: ViewMatrixData):
            data.distance = self.value

    class SetUpAxisIndex(Setter):
        def call(self, data: ViewMatrixData):
            data.up_axis_index = self.value

    class SetAngles(Setter):
        def call(self, data: ViewMatrixData):
            data.angles = self.value


class ProjMatrixData(object):
    def __init__(self, near_plane: float, far_plane: float, fov=60):
        self.plane = (near_plane, far_plane)
        self.fov = fov


class ProjMatrix(Matrix):

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

    class SetPlane(Setter):
        def call(self, data: ProjMatrixData):
            data.plane = self.value

    class SetFov(Setter):
        def call(self, data: ProjMatrixData):
            data.fov = self.value
