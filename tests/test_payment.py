"""Test payment object"""

from iliad_payment import Payment
from iliad_payment.core import Object
from TestHelper import TestHelper


class TestPayment(TestHelper):
    def test_class(self):
        assert issubclass(Payment, Object)
