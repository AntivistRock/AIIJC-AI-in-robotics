from source.engine import ILoader

from numpy import pi


class Table(ILoader):

    def _load(self):
        self.table = self.pb_client.loadURDF(
            'table/table.urdf',
            basePosition=[1.2, 0, 0],
            baseOrientation=self.pb_client.getQuaternionFromEuler([0, 0, pi / 2])
        )

    def _upload(self):
        pass
