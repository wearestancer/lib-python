"""Stub abstract object"""

from iliad_payment import Card
from iliad_payment.core import AbstractObject
from iliad_payment.core.decorators import populate_on_call


class StubObject(AbstractObject):
    _allowed_attributes = [
        'card1',
        'integer1',
        'string1',
        'string2',
    ]

    def force_modified(self, status):
        self._modified = status

        return self

    def force_populated(self, status):
        self._populated = status

        return self

    @property
    @populate_on_call
    def string1(self):
        return self._data.get('string1')

    @property
    @populate_on_call
    def string2(self):
        return self._data.get('string2')

    @string2.setter
    def string2(self, value):
        self._modified = True
        self._data['string2'] = value

    @property
    @populate_on_call
    def integer1(self):
        return self._data.get('integer1')

    @property
    def card1(self):
        return self._data.get('card1')

    @property
    def _init_card1(self):
        self._data['card1'] = Card()

        return self._data['card1']
