# -*- coding: utf-8 -*-

from .abstract_object import AbstractObject


class InnerSearchObject(AbstractObject):
    def __init__(self, base_object, inner_route):
        super().__init__()
        self.uri = f'{base_object.uri}/{inner_route}'

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, value) -> None:
        self._uri = value
