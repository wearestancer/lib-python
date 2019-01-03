"""Test card object"""

from iliad_payment import Card
from iliad_payment.core import Object

from random import randint
import pytest
import uuid


class TestCard:
    def test_class(self):
        assert issubclass(Card, Object)

    def test_id(self):
        assert Card().id is None

        id = uuid.uuid4().hex
        obj = Card(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = uuid.uuid4().hex

    def test_cvc(self):
        obj = Card()
        cvc = uuid.uuid4().hex[0:3]

        assert obj.cvc is None

        obj.cvc = cvc

        assert obj.cvc == cvc

        with pytest.raises(TypeError, match='CVC must have 3 characters'):
            obj.cvc = uuid.uuid4().hex[0:2]

        with pytest.raises(TypeError, match='CVC must be a string'):
            obj.cvc = randint(1, 100)
