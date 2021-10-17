from .i_resource import IResource


class ILoader(IResource):

    def __init__(self, pb_client):
        IResource.__init__(self)

        self.pb_client = pb_client

    def _update(self):
        pass
