"""Test dispute object"""

from iliad_payment import Dispute
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestDispute(TestHelper):
    def test_class(self):
        assert issubclass(Dispute, AbstractObject)
