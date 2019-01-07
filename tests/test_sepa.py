"""Test sepa object"""

from iliad_payment import Sepa
from iliad_payment.core import Object
from .TestHelper import TestHelper


class TestSepa(TestHelper):
    def test_class(self):
        assert issubclass(Sepa, Object)
