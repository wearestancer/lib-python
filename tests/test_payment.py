"""Test payment object"""

from iliad_payment import Payment
from iliad_payment.core import Object


class TestPayment:
    def test_class(self):
        assert issubclass(Payment, Object)
