"""Functional tests for customer object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import os
import pytest

from iliad_payment import Config
from iliad_payment import Customer
from iliad_payment.exceptions import NotFoundError
from ..TestHelper import TestHelper


@pytest.mark.skipif(
    os.getenv('API_KEY') is None,
    reason='Require an API key',
)
@pytest.mark.skipif(
    os.getenv('API_HOST') is None,
    reason='Require an API host',
)
class TestFunctionalCustomer(TestHelper):
    def setup_method(self, method):
        conf = Config()

        del conf.keys
        conf.keys = str(os.getenv('API_KEY'))
        conf.host = str(os.getenv('API_HOST'))
        conf.timeout = 1

    def test_get(self):
        with pytest.raises(NotFoundError):
            obj = Customer(self.random_string(29))
            obj.name

        obj = Customer('cust_aEBF8w2szNdhreJ0uEmrplen')

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
