"""Functional tests for customer object"""

import pytest
import uuid

from stancer import Customer
from stancer.exceptions import NotFoundError
from .TestHelper import TestHelper


class TestFunctionalCustomer(TestHelper):
    def test_get(self):
        with pytest.raises(NotFoundError) as error:
            obj = Customer(self.random_string(29))
            obj.name

        assert error.value.message == 'No such customer {}'.format(obj.id)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404
        assert error.value.type == 'invalid_request_error'

        obj = Customer('cust_9y1U3mHPd1yPvbx07VBRqd9C')

        assert obj.name == 'John Doe'
        assert obj.email == 'john.doe@example.com'
        assert obj.mobile == '+33666172730'  # Random generated number

    def test_send(self):
        obj = Customer()

        tmp = self.random_string(5)
        name = 'John Doe ({})'.format(tmp)
        email = 'john.doe+{}@example.com'.format(tmp)
        external_id = uuid.uuid4()
        mobile = self.random_mobile()

        obj.name = name
        obj.email = email
        obj.external_id = external_id
        obj.mobile = mobile

        assert obj.id is None
        assert obj.send() == obj
        assert obj.id is not None
        assert obj.id.startswith('cust_')

        uid1 = obj.id

        # If sent, we can get it
        obj = Customer(uid1)

        assert obj.name == name
        assert obj.email == email
        assert obj.external_id == str(external_id)
        assert obj.mobile == mobile

        # External ID does not prevent duplication
        obj = Customer()

        tmp = self.random_string(5)
        name = 'John Doe ({})'.format(tmp)
        email = 'john.doe+{}@example.com'.format(tmp)

        obj.name = name
        obj.email = email
        obj.external_id = external_id

        assert obj.id is None
        assert obj.send() == obj
        assert obj.id is not None
        assert obj.id.startswith('cust_')
        assert obj.id != uid1

        uid2 = obj.id

        # Clean
        for uid in (uid1, uid2):
            obj = Customer(uid)

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
        assert obj.send() == obj
        assert obj.id is not None
        assert obj.name is None
        assert obj.email is None
        assert obj.mobile == mobile

        obj.name = name
        obj.send()

        assert obj.name == name
        assert obj.email is None
        assert obj.mobile == mobile

        obj.email = email
        obj.mobile = self.random_mobile()
        obj.send()

        assert obj.name == name
        assert obj.email == email
        assert obj.mobile != mobile

        # Clean it
        assert obj.delete() == obj
        assert obj.id is None
