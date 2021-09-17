from __future__ import absolute_import
from __future__ import division

from .nn_model import SimpleRecurrentAgent
# from .teapot_detectron import TeapotDetectron

import functools
import inspect


class Model(object):

    def __init__(self):

        self.simple_rec_agent = SimpleRecurrentAgent((128, 128), 10)
        # self.detectron = TeapotDetectron()

    def __getattr__(self, name):
        """Inject the client id into Bullet functions."""
        attribute = getattr(self.simple_rec_agent, name)

        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute)

        return attribute
