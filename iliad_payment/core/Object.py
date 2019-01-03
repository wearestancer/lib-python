# -*- coding: utf-8 -*-


class Object:
    """Manage common code between API object"""

    def __init__(self, id=None):
        self._id = id
        self._data = {}

    @property
    def id(self):
        return self._id
