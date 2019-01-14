"""Test customer object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment import Customer
from iliad_payment.core import AbstractObject, AbstractName
from .TestHelper import TestHelper


class TestCustomer(TestHelper):
    def test_class(self):
        assert issubclass(Customer, AbstractObject)
        assert issubclass(Customer, AbstractName)

    def test_email(self):
        obj = Customer()
        email = self.random_string(10)

        assert obj.email is None

        obj.email = email

        assert obj.email == email

        with pytest.raises(
            TypeError,
            match='Email must be a string',
        ):
            obj.email = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='Email must be have at between 5 and 64 characters',
        ):
            obj.email = self.random_string(4)

        with pytest.raises(
            TypeError,
            match='Email must be have at between 5 and 64 characters',
        ):
            obj.email = self.random_string(65, 70)

    def test_mobile(self):
        obj = Customer()
        mobile = self.random_mobile()

        assert obj.mobile is None

        obj.mobile = mobile

        assert obj.mobile == mobile

        with pytest.raises(
            TypeError,
            match='Mobile phone must be a string',
        ):
            obj.mobile = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='Mobile phone must be have at between 8 and 16 characters',
        ):
            obj.mobile = self.random_string(7)

        with pytest.raises(
            TypeError,
            match='Mobile phone must be have at between 8 and 16 characters',
        ):
            obj.mobile = self.random_string(17)

    def test_uri(self):
        obj = Customer()
        id = self.random_string(29)

        assert obj.uri == 'https://api.iliad78.net/v1/customers'

        obj.hydrate({'id': id})

        assert obj.uri == 'https://api.iliad78.net/v1/customers/' + id

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
