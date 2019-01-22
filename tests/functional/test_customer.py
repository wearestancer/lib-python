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
        conf.keys = os.getenv('API_KEY')
        conf.host = os.getenv('API_HOST')

    def test_get(self):
        with pytest.raises(NotFoundError):
            obj = Customer(self.random_string(29))
            obj.name

        obj = Customer('cust_aEBF8w2szNdhreJ0uEmrplen')

        assert obj.name == 'John Doe'
        assert obj.email == 'john.doe@example.com'
        assert obj.mobile == '+33666172730'  # Random generated number
