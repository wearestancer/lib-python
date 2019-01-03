"""Test sepa object"""

from iliad_payment import Sepa
from iliad_payment.core import Object


class TestSepa:
    def test_class(self):
        assert issubclass(Sepa, Object)
