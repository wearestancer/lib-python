"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from datetime import datetime
import pytest

from iliad_payment import Card
from .stub.object import Object
from .TestHelper import TestHelper


class TestObject(TestHelper):
    def test_id(self):
        assert Object().id is None

        id = self.random_string(29)
        obj = Object(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_hydrate(self):
        obj = Object()
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
