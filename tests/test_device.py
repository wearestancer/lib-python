"""Test device object"""

import pytest
import responses

from iliad_payment import Device
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestDevice(TestHelper):
    def test_class(self):
        assert issubclass(Device, AbstractObject)
