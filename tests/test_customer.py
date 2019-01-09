"""Test customer object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pytest

from iliad_payment import Customer
from iliad_payment.core import Object
from .TestHelper import TestHelper


class TestCustomer(TestHelper):
    def test_class(self):
        assert issubclass(Customer, Object)

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

    def test_name(self):
        obj = Customer()
        name = self.random_string(10)

        assert obj.name is None

        obj.name = name

        assert obj.name == name

        with pytest.raises(
            TypeError,
            match='Name must be a string',
        ):
            obj.name = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='Name must be have at between 4 and 64 characters',
        ):
            obj.name = self.random_string(3)

        with pytest.raises(
            TypeError,
            match='Name must be have at between 4 and 64 characters',
        ):
            obj.name = self.random_string(65, 70)
