"""Test customer object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest
import responses

from iliad_payment import Customer
from iliad_payment.core import AbstractObject, AbstractName
from .TestHelper import TestHelper


class TestCustomer(TestHelper):
    def test_class(self):
        assert issubclass(Customer, AbstractObject)
        assert issubclass(Customer, AbstractName)

    @responses.activate
    def test_email(self):
        obj = Customer()
        email = self.random_string(10)

        assert obj.email is None
        assert obj.is_not_modified

        obj.email = email

        assert obj.email == email
        assert obj.is_modified

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

        obj = Customer(self.random_string(29))
        params = {
            'email': self.random_string(20),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.email == params['email']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_mobile(self):
        obj = Customer()
        mobile = self.random_mobile()

        assert obj.mobile is None
        assert obj.is_not_modified

        obj.mobile = mobile

        assert obj.mobile == mobile
        assert obj.is_modified

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

        obj = Customer(self.random_string(29))
        params = {
            'mobile': self.random_mobile(),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.mobile == params['mobile']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_name(self):
        # More test on test_abstract_name
        # Here we are just testing the modified flag and auto population

        obj = Customer()
        name = self.random_string(4, 64)

        assert obj.is_not_modified

        obj.name = name

        assert obj.name == name
        assert obj.is_modified

        obj = Customer(self.random_string(29))
        params = {
            'name': self.random_string(30),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.name == params['name']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_uri(self):
        obj = Customer()
        uid = self.random_string(29)

        assert obj.uri == 'https://api.iliad78.net/v1/customers'

        obj.hydrate({'id': uid})

        assert obj.uri == 'https://api.iliad78.net/v1/customers/' + uid

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
