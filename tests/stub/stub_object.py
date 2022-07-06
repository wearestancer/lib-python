"""Stub abstract object"""

from stancer import Card
from stancer.core import AbstractObject
from stancer.core.decorators import populate_on_call


class StubObject(AbstractObject):
    _ENDPOINT = 'stub'

    _allowed_attributes = [
        'card1',
        'card2',
        'cards',
        'integer1',
        'string1',
        'string2',
    ]

    def force_modified(self, *args):
        self._modified.add(*args)

        return self

    def force_populated(self, status):
        self._populated = status

        return self

    def reset_modified(self):
        del self._modified

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
        self._modified.add('string2')
        self._data['string2'] = value

    @property
    @populate_on_call
    def integer1(self):
        return self._data.get('integer1')

    @property
    def card1(self):
        return self._data.get('card1')

    @property
    def _init_card1(self) -> Card:
        return Card

    @property
    def card2(self):
        return self._data.get('card2')

    @card2.setter
    def card2(self, value):
        self._modified.add('card2')
        self._data['card2'] = value

    @property
    def _init_card2(self) -> Card:
        return Card

    @property
    @populate_on_call
    def cards(self):
        return self._data.get('cards', [])

    @property
    def _init_cards(self) -> Card:
        return Card
