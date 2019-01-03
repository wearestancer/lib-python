"""Test customer object"""

from iliad_payment import Customer
from iliad_payment.core import Object


class TestCustomer:
    def test_class(self):
        assert issubclass(Customer, Object)
