"""Functional tests for payment object"""

from __future__ import unicode_literals
from builtins import str

import os
import platform
import pytest
import random

from iliad_payment import Card
from iliad_payment import Config
from iliad_payment import Customer
from iliad_payment import Payment
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
class TestFunctionalPayment(TestHelper):
    def get_card_number(self):
        cards = [
            '4242424242424242',
            '5555555555554444',
            '4000000760000002',
            '4000001240000000',
            '4000004840000008',
            '4000000400000008',
            '4000000560000004',
            '4000002080000001',
            '4000002460000001',
            '4000002500000003',
            '4000002760000016',
            '4000003720000005',
            '4000003800000008',
            '4000004420000006',
            '4000005280000002',
            '4000005780000007',
            '4000006200000007',
            '4000006430000009',
            '4000007240000007',
            '4000007520000008',
            '4000007560000009',
            '4000008260000000',
            '4000000360000006',
            '4000001560000002',
            '4000003440000004',
            '4000003920000003',
            '3530111333300000',
            '4000005540000008',
            '4000007020000003',
        ]

        return random.choice(cards)

    def setup_method(self, method):
        conf = Config()

        del conf.keys
        conf.keys = str(os.getenv('API_KEY'))
        conf.host = str(os.getenv('API_HOST'))
        conf.timeout = 1

    def test_get(self):
        # 404 with an unknown payment (with a random id)
        with pytest.raises(NotFoundError) as error:
            obj = Payment(self.random_string(29))
            obj.amount

        assert error.value.status_code == 404
        assert error.value.reason == 'Not Found'
        assert error.value.type == 'invalid_request_error'
        assert isinstance(error.value.message, dict)
        message = 'No such payment {}'.format(obj.id)
        assert error.value.message['id'] == message

        # Recover a valid payment
        obj = Payment('paym_FQgpGVJpyGPVJVIuQtO3zy6i')

        assert obj.amount == 7810
        assert obj.currency == 'usd'
        assert obj.description == 'Automatic test, 78.10 USD'
        assert obj.method == 'card'

        assert isinstance(obj.card, Card)
        assert obj.card.id == 'card_nsA0eap90E6HRod6j54pnVWg'

        assert isinstance(obj.customer, Customer)
        assert obj.customer.id == 'cust_6FbQaYtxjADzerqdO5gs79as'

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_save(self, currency):
        obj = Payment()

        amount = self.random_integer(50, 10000)
        desc = 'Python {} automatic test, {:.2f} {}'.format(
            platform.python_version(),
            amount / 100,
            currency.upper(),
        )

        card = Card()
        card.number = self.get_card_number()
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.cvc = str(self.random_integer(100, 999))

        customer = Customer()
        customer.name = 'John Doe'
        customer.email = 'john.doe@example.com'

        obj.amount = amount
        obj.card = card
        obj.currency = currency
        obj.customer = customer
        obj.description = desc

        assert obj.id is None
        assert obj.save() == obj
        assert obj.id is not None

        uid = obj.id
        card_uid = card.id
        customer_uid = customer.id

        # If saved, we can get it
        obj = Payment(uid)

        assert obj.amount == amount
        assert obj.currency == currency
        assert obj.description == desc

        assert obj.card.id == card_uid
        assert obj.customer.id == customer_uid
