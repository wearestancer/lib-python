"""Functional tests for customer object"""

import datetime
import uuid

import pytest

from stancer.core.enum.version import Version
from stancer.customer import Customer
from stancer.exceptions import NotFoundError

from .FunctionalTestHelper import FunctionalTestHelper


class TestFunctionalCustomer(FunctionalTestHelper):
    def test_get(self):
        with pytest.raises(NotFoundError) as error:
            customer = Customer(f'cust_{self.random_string(24)}')
            assert customer.name

        assert error.value.message == self.get_not_found_message(customer)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404

        customer = Customer('cust_iUkhjL9K2bTb436NdKSdqCYv')

        assert customer.name == 'John Doe'
        assert customer.email == 'john.doe@example.com'
        assert customer.mobile == '+33666172730'  # Random generated number

    def test_send(self):
        customer = Customer()

        tmp = self.random_string(5)
        name = f'John Doe ({tmp})'
        email = f'john.doe+{tmp}@example.com'
        external_id = uuid.uuid4()
        mobile = self.random_mobile()
        date_birth = datetime.date(1993, 10, 25)
        customer.name = name
        customer.email = email
        customer.external_id = external_id
        customer.mobile = mobile
        customer.date_birth = date_birth

        assert customer.id is None
        assert customer.send() == customer
        assert customer.id is not None
        assert customer.id.startswith('cust_')

        uid1 = customer.id

        # If sent, we can get it
        customer = Customer(uid1)

        assert customer.name == name
        assert customer.email == email
        assert customer.external_id == str(external_id)
        assert customer.mobile == mobile
        assert customer.date_birth == date_birth

        # External ID does not prevent duplication
        customer = Customer()

        tmp = self.random_string(5)
        name = f'John Doe ({tmp})'
        email = f'john.doe+{tmp}@example.com'
        mobile = self.random_mobile()

        customer.name = name
        customer.email = email
        customer.external_id = external_id
        customer.mobile = mobile

        assert customer.id is None
        assert customer.send() == customer
        assert customer.id is not None
        assert customer.id.startswith('cust_')
        assert customer.id != uid1

        uid2 = customer.id

        customer2 = Customer(uid2)
        assert customer2.id == uid2  # id is still the same
        assert customer2.name == name
        assert not customer2.deleted
        assert customer2.email == email
        assert customer2.mobile == mobile

        # We can not valid values heres.
        assert customer2.created is not None

        # We can create a fully completed customer. Except Country
        customer3 = Customer()
        date_birth3 = datetime.datetime(
            year=self.random_year() - 50,
            month=self.random_integer(1, 12),
            day=self.random_integer(1, 28),
        ).date()
        email3 = f'john.doe+{tmp}3@example.com'
        external_id3 = uuid.uuid4()
        legal_id3 = self.random_string(16)
        mobile3 = self.random_mobile()
        name3 = f'John Doe ({tmp})'

        customer3.date_birth = date_birth3
        customer3.email = email3
        customer3.external_id = external_id3
        customer3.legal_id = legal_id3
        customer3.mobile = mobile3
        customer3.name = name3

        assert customer3.id is None
        assert customer3.send() == customer3
        assert customer3.id is not None
        assert customer3.date_birth == date_birth3
        assert customer3.email == email3
        assert customer3.external_id == str(external_id3)
        assert not customer3.deleted
        assert customer3.legal_id == legal_id3
        assert customer3.mobile == mobile3
        assert customer3.name == name3

        uid3 = customer3.id
        # # Clean
        for uid in (uid1, uid2, uid3):
            customer = Customer(uid)
            id = customer.id
            assert customer.delete()
            assert id in (uid1, uid2, uid3)
            # Warning conditional in test. when we delete a customer in V1 we just delete and cannot access it anymore
            assert (
                customer.deleted is None
                if self.conf.version == Version.API_V1
                else True
            )

    def test_update_delete(self):
        customer = Customer()

        tmp = self.random_string(5)
        name = f'John Doe ({tmp})'
        email = f'john.doe+{tmp}@example.com'
        mobile = self.random_mobile()

        customer.mobile = mobile

        assert customer.id is None
        assert customer.send() == customer
        assert customer.id is not None
        assert customer.name is None
        assert customer.email is None
        assert customer.mobile == mobile

        customer.name = name
        customer.send()

        assert customer.name == name
        assert customer.email is None
        assert customer.mobile == mobile

        customer.email = email
        mobile2 = self.random_mobile()
        customer.mobile = mobile2
        customer.send()

        assert customer.name == name
        assert customer.email == email
        assert customer.mobile != mobile
        assert customer.mobile == mobile2
        id = customer.id

        # Clean it
        assert customer.delete()
        # Warning conditional in test, Deletion in V1 cannot be retrieve.
        if self.conf.version != Version.API_V1:
            assert customer.id == id
            assert customer.name == name
            assert customer.email == email
            assert customer.mobile == mobile2

            with pytest.raises(NotFoundError) as error:
                customer.send()

            assert error.value.message == self.get_not_found_message(customer)
            assert error.value.reason == 'Not Found'
            assert error.value.status_code == 404
