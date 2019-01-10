"""Test payment object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment import Payment
from iliad_payment.core import AbstractObject, AbstractAmount
from .TestHelper import TestHelper


class TestPayment(TestHelper):
    def test_class(self):
        assert issubclass(Payment, AbstractObject)
        assert issubclass(Payment, AbstractAmount)
