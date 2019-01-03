# -*- coding: utf-8 -*-

from .core.Object import Object


class Card(Object):
    """Representation of a card"""

    @property
    def cvc(self):
        return self._data.get('cvc', None)

    @cvc.setter
    def cvc(self, value):
        if type(value) != str:
            raise TypeError('CVC must be a string')

        if len(value) != 3:
            raise TypeError('CVC must have 3 characters')

        self._data['cvc'] = value
