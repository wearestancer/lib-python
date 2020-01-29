"""Test refund object"""

from iliad_payment import Refund
from iliad_payment.core import AbstractAmount
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestRefund(TestHelper):
    def test_class(self):
        assert issubclass(Refund, AbstractAmount)
        assert issubclass(Refund, AbstractObject)

        assert Refund._ENDPOINT == 'refunds'
