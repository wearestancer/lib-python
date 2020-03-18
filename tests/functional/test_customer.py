"""Functional tests for customer object"""

import pytest

from iliad_payment import Customer
from iliad_payment.exceptions import NotFoundError
from .TestHelper import TestHelper


class TestFunctionalCustomer(TestHelper):
    def test_get(self):
        with pytest.raises(NotFoundError) as error:
            obj = Customer(self.random_string(29))
            obj.name

        assert error.value.status_code == 404
        assert error.value.reason == 'Not Found'
        assert error.value.type == 'invalid_request_error'
        assert isinstance(error.value.message, dict)
        message = 'No such customer {}'.format(obj.id)
        assert error.value.message['id'] == message

        obj = Customer('cust_9y1U3mHPd1yPvbx07VBRqd9C')

        assert obj.name == 'John Doe'
        assert obj.email == 'john.doe@example.com'
        assert obj.mobile == '+33666172730'  # Random generated number

    def test_save(self):
        obj = Customer()

        tmp = self.random_string(5)
        name = 'John Doe ({})'.format(tmp)
        email = 'john.doe+{}@example.com'.format(tmp)
        mobile = self.random_mobile()

        obj.name = name
        obj.email = email
        obj.mobile = mobile

        assert obj.id is None
        assert obj.save() == obj
        assert obj.id is not None

        uid = obj.id

        # If saved, we can get it
        obj = Customer(uid)

        assert obj.name == name
        assert obj.email == email
        assert obj.mobile == mobile

        # Clean it
        assert obj.delete() == obj
        assert obj.id is None

    def test_update(self):
        obj = Customer()

        tmp = self.random_string(5)
        name = 'John Doe ({})'.format(tmp)
        email = 'john.doe+{}@example.com'.format(tmp)
        mobile = self.random_mobile()

        obj.mobile = mobile

        assert obj.id is None
        assert obj.save() == obj
        assert obj.id is not None
        assert obj.name is None
        assert obj.email is None
        assert obj.mobile == mobile

        obj.name = name
        obj.save()

        assert obj.name == name
        assert obj.email is None
        assert obj.mobile == mobile

        obj.email = email
        obj.mobile = self.random_mobile()
        obj.save()

        assert obj.name == name
        assert obj.email == email
        assert obj.mobile != mobile

        # Clean it
        assert obj.delete() == obj
        assert obj.id is None
