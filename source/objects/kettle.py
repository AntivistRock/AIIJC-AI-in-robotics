import source.engine as engine

from source.utils import rotate

import os
import numpy as np


class Kettle(engine.ILoader):

    def _load(self):

        # y_pos = np.random.uniform(-0.5, 0.25)
        y_pos = 0

        os.chdir(os.path.dirname(__file__))
        print(f"Kittle: {os.getcwd()}")

        self.kettle = self.pb_client.loadURDF(
            r"./source/ext/objects/kettle/urdf/kettle.urdf",
            basePosition=[0.85, y_pos, 0.86],
            baseOrientation=self.pb_client.getQuaternionFromEuler([np.pi / 2, 0, -np.pi / 2.4])
        )

    def _upload(self):
        pass

    def get_handle_pos(self):
        curr_pos, curr_orient = self.pb_client.getBasePositionAndOrientation(self.kettle)
        curr_orient = list(self.pb_client.getEulerFromQuaternion(curr_orient))
        handle_pos = np.array(curr_pos) + rotate([-0.15, 0, 0], curr_orient)
        return handle_pos
