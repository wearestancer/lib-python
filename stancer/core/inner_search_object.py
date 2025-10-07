# -*- coding: utf-8 -*-

from . import AbstractObject


class InnerSearchObject(AbstractObject):
    def __init__(self, base_object, inner_route):
        super().__init__()
        self.uri = f'{base_object.uri}/{inner_route}'

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value
