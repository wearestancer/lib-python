"""Test customer object"""

import pytest
import responses
import uuid

from stancer import Customer
from stancer.core import AbstractCountry
from stancer.core import AbstractObject
from stancer.core import AbstractName
from stancer.exceptions import InvalidCustomerEmailError
from stancer.exceptions import InvalidCustomerExternalIdError
from stancer.exceptions import InvalidCustomerMobileError
from .TestHelper import TestHelper


class TestCustomer(TestHelper):
    def test_class(self):
        assert issubclass(Customer, AbstractCountry)
        assert issubclass(Customer, AbstractName)
        assert issubclass(Customer, AbstractObject)

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
            InvalidCustomerEmailError,
            match='Email must be a string.',
        ):
            obj.email = self.random_integer(20)

        with pytest.raises(
            InvalidCustomerEmailError,
            match='Email must be between 5 and 64 characters.',
        ):
            obj.email = self.random_string(4)

        with pytest.raises(
            InvalidCustomerEmailError,
            match='Email must be between 5 and 64 characters.',
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
    def test_external_id(self):
        obj = Customer()
        external_id = self.random_string(36)

        assert obj.external_id is None

        obj.external_id = external_id

        assert obj.external_id == external_id

        with pytest.raises(
            InvalidCustomerExternalIdError,
            match='External ID must be a string.',
        ):
            obj.external_id = self.random_integer(20)

        with pytest.raises(
            InvalidCustomerExternalIdError,
            match='External ID must be 36 characters maximum.',
        ):
            obj.external_id = self.random_string(40)

        obj = Customer(self.random_string(29))
        params = {
            'external_id': self.random_string(36),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.external_id == params['external_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

        # Works with uuid

        obj = Customer()
        external_id = uuid.uuid4()

        assert obj.external_id is None

        obj.external_id = external_id

        assert obj.external_id == str(external_id)

    def test_is_complete(self):
        email = self.random_string(5, 64)
        name = self.random_string(4, 64)
        mobile = self.random_mobile()

        # Empty customer is not complete
        assert Customer().is_complete is False
        assert Customer().is_not_complete is True

        # Only email => complete
        obj = Customer()

        obj.email = email
        # obj.name
        # obj.mobile

        assert obj.is_complete is True
        assert obj.is_not_complete is False

        # Only name => incomplete
        obj = Customer()

        # obj.email
        obj.name = name
        # obj.mobile

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Only mobile => complete
        obj = Customer()

        # obj.email
        # obj.name
        obj.mobile = mobile

        assert obj.is_complete is True
        assert obj.is_not_complete is False

        # Of course, will all => complete
        obj = Customer()

        obj.email = email
        obj.name = name
        obj.mobile = mobile

        assert obj.is_complete is True
        assert obj.is_not_complete is False

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
            InvalidCustomerMobileError,
            match='Mobile phone must be a string.',
        ):
            obj.mobile = self.random_integer(20)

        with pytest.raises(
            InvalidCustomerMobileError,
            match='Mobile phone must be between 8 and 16 characters.',
        ):
            obj.mobile = self.random_string(7)

        with pytest.raises(
            InvalidCustomerMobileError,
            match='Mobile phone must be between 8 and 16 characters.',
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

        assert obj.uri == 'https://api.stancer.com/v1/customers'

        obj.hydrate(id=uid)

        assert obj.uri == 'https://api.stancer.com/v1/customers/' + uid

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
