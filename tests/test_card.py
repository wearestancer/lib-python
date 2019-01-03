"""Test card object"""

from iliad_payment import Card
from iliad_payment.core import Object


class TestCard:
    def test_class(self):
        assert issubclass(Card, Object)
