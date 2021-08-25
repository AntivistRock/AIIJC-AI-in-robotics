class Resource (object):

    def __init__(self):
        self._is_load = False

    def __del__(self):
        if self._is_load:
            self.upload()

    def load(self):
        self._load()
        self._is_load = True

    def upload(self):
        self._upload()
        self._is_load = False

    def update(self):
        if not self._is_load:
            self.load()

        self._update()

    # TODO: write decorator from NotImplementedError

    def _load(self):
        raise NotImplementedError()

    def _upload(self):
        raise NotImplementedError()

    def _update(self):
        raise NotImplementedError()
