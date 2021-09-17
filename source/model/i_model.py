from .nn_model import SimpleRecurrentAgent
from .teapot_detectron import TeapotDetectron


class Model(object):

    def __init__(self):

        self.simple_rec_agent = SimpleRecurrentAgent((128, 128), 10)
        self.detectron = TeapotDetectron()

    def predict(self):
        return []
