import pybullet as pb

from source.utils import rotate

from .i_matrix import IMatrix


class ContractVMArgs(object):
    def __init__(self, camera_pos, target_pos, up_vector):
        self.camera_pos = camera_pos
        self.target_pos = target_pos
        self.vector_up = up_vector


class ViewMatrixData(object):
    def __init__(self, position, angles, up_vector, orient, offset):
        super().__init__()

        self.position = position
        self.angles = angles
        self.up_vector = up_vector
        self.orient = orient
        self.offset = offset

    def get(self) -> ContractVMArgs:
        angles = [-self.angles[0], -self.angles[1], -self.angles[2]]

        orient_rot = rotate(self.orient, angles)
        offset_rot = rotate(self.offset, angles)

        camera_pos = self.position + offset_rot
        target_pos = camera_pos + orient_rot
        up_vector = self.up_vector

        return ContractVMArgs(camera_pos, target_pos, up_vector)


class ViewMatrix(IMatrix):

    def __init__(self, data: ViewMatrixData):
        self.data = data
        super().__init__()

    def _update(self):
        args = self.data.get()
        self._matrix = pb.computeViewMatrix(
            args.camera_pos,
            args.target_pos,
            args.vector_up
        )
