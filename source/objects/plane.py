from source.engine import ILoader


class Plane(ILoader):

    def _load(self):
        self.plane = self.pb_client.loadURDF('plane.urdf')

    def _upload(self):
        pass
