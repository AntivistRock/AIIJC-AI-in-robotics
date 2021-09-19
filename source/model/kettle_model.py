from __future__ import absolute_import
from __future__ import division

from .nn_model import SimpleRecurrentAgent
# from .teapot_detectron import TeapotDetectron

import functools
import inspect


class KettleModel(object):

    def __init__(self):

        self.simple_rec_agent = SimpleRecurrentAgent((128, 128), 10)
        # self.detectron = TeapotDetectron()

    def __getattr__(self, name):

        attribute = getattr(self.simple_rec_agent, name)

        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute)

        return attribute
