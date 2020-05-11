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

    def test_country(self):
        obj = Device()
        country = self.random_string(10)

        assert obj.country is None

        obj.country = country

        assert obj.country == country
        assert obj.to_json().find('"country":"{}"'.format(country)) > 0

    def test_http_accept(self):
        obj = Device()
        http_accept = self.random_string(10)

        assert obj.http_accept is None

        obj.http_accept = http_accept

        assert obj.http_accept == http_accept
        assert obj.to_json().find('"http_accept":"{}"'.format(http_accept)) > 0
