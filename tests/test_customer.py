"""Test customer object"""

from iliad_payment import Customer
from iliad_payment.core import Object
from .TestHelper import TestHelper


class TestCustomer(TestHelper):
    def test_class(self):
        assert issubclass(Customer, Object)
