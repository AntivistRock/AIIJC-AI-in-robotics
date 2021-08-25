from .resource import Resource


class Loader(Resource):

    def _load(self):
        raise NotImplementedError("Loader must be implemented method 'Loader._load()'")

    def _upload(self):
        pass

    def _update(self):
        pass
