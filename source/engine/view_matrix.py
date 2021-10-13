import pybullet as pb

import utils
from .i_matrix import IMatrix


class ContractVMArgs(object):
    def __init__(self, camera_pos, target_pos, up_vector):
        self.camera_pos = camera_pos
        self.target_pos = target_pos
        self.vector_up = up_vector


class ViewMatrixData(utils.IComutating):
    def __init__(self, position, angles, up_vector, orient, offset):
        super().__init__()

        self.position = position
        self.angles = angles
        self.up_vector = up_vector
        self.orient = orient
        self.offset = offset

    def get(self) -> ContractVMArgs:
        orient_rot = utils.rotate(self.orient, self.angles)
        offset_rot = utils.rotate(self.offset, self.angles)

        camera_pos = self.position + offset_rot
        target_pos = camera_pos + orient_rot
        up_vector = self.up_vector

        return ContractVMArgs(camera_pos, target_pos, up_vector)

    class SetCameraPos(utils.ISetter):
        def call(self, data):
            data.position = self.value

    class SetEulerAngles(utils.ISetter):
        def call(self, data):
            data.angles = self.value

    class SetUpVector(utils.ISetter):
        def call(self, data):
            data.up_vector = self.value

    class SetOrient(utils.ISetter):
        def call(self, data):
            data.orient = self.value


class ViewMatrix(IMatrix):

    def __init__(self, data: ViewMatrixData):
        self._data = data
        self.data_com = data.get_com()
        super().__init__()

    def _update(self):
        args = self._data.get()
        self._matrix = pb.computeViewMatrix(
            args.camera_pos,
            args.target_pos,
            args.vector_up
        )

    def update_set(self, setters):
        for setter in setters:
            self.data_com.action(setter)

        self._update()
