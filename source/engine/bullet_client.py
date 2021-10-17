from __future__ import absolute_import
from __future__ import division

import functools
import inspect
import os

import pybullet


class BulletClient(object):

    def __init__(self, connection_mode=None, key=None, options=''):

        self._shapes = {}
        self._pid = os.getpid()

        if connection_mode is None:
            self._client = pybullet.connect(pybullet.SHARED_MEMORY, key=key, options=options)
            if self._client >= 0:
                return
            else:
                connection_mode = pybullet.DIRECT

        if key:
            self._client = pybullet.connect(connection_mode, key=key, options=options)
        else:
            self._client = pybullet.connect(connection_mode, options=options)

    def __del__(self):
        if self._client >= 0 and self._pid == os.getpid():
            try:
                pybullet.disconnect(physicsClientId=self._client)
                self._client = -1
            except pybullet.error:
                pass

    def __getattr__(self, name):
        attribute = getattr(pybullet, name)
        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute, physicsClientId=self._client)
        if name == "disconnect":
            self._client = -1
        return attribute
