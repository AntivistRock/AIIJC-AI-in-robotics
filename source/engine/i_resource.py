class IResource(object):

    def __init__(self):
        self._is_load = False

    def __del__(self):
        if self._is_load:
            self.upload()

    def load(self):
        if not self._is_load:
            self._is_load = True
            self._load()

    def upload(self):
        if self._is_load:
            self._upload()
            self._is_load = False

    def update(self):
        if not self._is_load:
            raise RuntimeError("Resource isn't loaded")
        return self._update()

    # @must_be_implemented
    def _load(self):
        raise NotImplementedError()

    # @must_be_implemented
    def _upload(self):
        raise NotImplementedError()

    # @must_be_implemented
    def _update(self):
        raise NotImplementedError()
