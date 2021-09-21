import engine
import numpy as np


class Kettle(engine.ILoader):

    def __init__(self, pb_client):
        engine.ILoader.__init__(self)
        self.pb_client = pb_client

    def _load(self):

        x_pos = np.random.uniform(-0.30, 0.16)

        self.kettle = self.pb_client.loadURDF(r"./ext/objects/kettle/urdf/kettle.urdf",
                                              basePosition=[x_pos, 0.85, 0.85],
                                              baseOrientation=self.pb_client.getQuaternionFromEuler(
                                                  [np.pi / 2, 0, np.pi / 10]))
        self.last_z = self.get_z_coordinate()
        self.delta_z = 0

    def _update(self):
        new_z = self.get_z_coordinate()
        self.delta_z = new_z - self.last_z
        self.last_z = new_z

    def get_handle_pos(self):
        handle_pos = self.pb_client.getBasePositionAndOrientation(self.kettle)[0]
        handle_pos[0] += 0.07
        handle_pos[2] += 0.07
        return handle_pos

    def get_z_coordinate(self):
        return self.pb_client.getBasePositionAndOrientation(self.kettle)[0][2]
