"""Test core object"""

from iliad_payment import core


class Object(core.Object):
    @property
    def string1(self):
        return self._data.get('string1', None)

    @property
    def integer1(self):
        return self._data.get('integer1', None)

    @property
    def card1(self):
        return self._data.get('card1', None)
