"""Test device object"""

import pytest

from iliad_payment import Device
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestDevice(TestHelper):
    def test_class(self):
        assert issubclass(Device, AbstractObject)

    def test_city(self):
        obj = Device()
        city = self.random_string(10)

        assert obj.city is None

        obj.city = city

        assert obj.city == city
        assert obj.to_json().find('"city":"{}"'.format(city)) > 0
