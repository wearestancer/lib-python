"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
from datetime import datetime
import pytest

from iliad_payment import Card
from .stub.stub_object import StubObject
from .TestHelper import TestHelper


class TestObject(TestHelper):
    def test__dict__(self):
        obj = StubObject()
        card = Card(self.random_string(29))

        card.number = '4242424242424242'

        params = {
            'id': self.random_string(29),
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': card,
            'created': 1546867615,
        }

        obj.hydrate(params)

        result = obj.__dict__

        assert isinstance(result, dict)

        assert 'id' in result
        assert result['id'] == params['id']

        assert 'string1' in result
        assert result['string1'] == params['string1']

        assert 'integer1' in result
        assert result['integer1'] == params['integer1']

        assert 'created' in result
        assert result['created'] == '2019-01-07 14:26:55'

        assert 'card1' in result
        assert isinstance(result['card1'], dict)

        assert 'id' in result['card1']
        assert result['card1']['id'] == card.id

        assert 'number' in result['card1']
        assert result['card1']['number'] == card.number

    def test_id(self):
        assert StubObject().id is None

        id = self.random_string(29)
        obj = StubObject(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_hydrate(self):
        obj = StubObject()
        card = Card()
        id = self.random_string(29)

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': card,
            'created': 1546867615,
        }

        assert obj.hydrate(params) == obj

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']

        assert isinstance(obj.created, datetime)
        assert obj.created.year == 2019
        assert obj.created.month == 1
        assert obj.created.day == 7
        assert obj.created.hour == 14
        assert obj.created.minute == 26
        assert obj.created.second == 55

        assert obj.card1 == card
        assert card.id is None

        assert obj.hydrate({'card1': id}) == obj

        assert obj.card1 == card
        assert card.id == id

    def test_to_json(self):
        obj = StubObject()
        card = Card()

        card.hydrate({
            'number': '4242424242424242',
            'brand': self.random_string(10),
        })

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': card,
            'created': 1546867615,
        }

        obj.hydrate(params)

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"string1":"{}"'.format(params['string1'])) > 0
        assert result.find('"integer1":{}'.format(params['integer1'])) > 0
        assert result.find('"card1":{{"number":"{}"}}'.format(card.number)) > 0
        assert result.find('"created"') == -1

        card.hydrate({'id': self.random_string(29)})

        result = obj.to_json()

        assert result.find('"card1":{{"id":"{}"}}'.format(card.id)) > 0

        id = self.random_string(29)
        obj.hydrate({'id': id})

        result = obj.to_json()

        assert result == '{{"id":"{}"}}'.format(id)
