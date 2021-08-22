import pybullet as pb


class PyBulletClient (object):

    def __init__(self, connection_type):
        self.id = pb.connect(connection_type)

    def __del__(self):
        pb.disconnect(self.id)
