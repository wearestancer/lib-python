"""Functional tests for refunds"""

from __future__ import unicode_literals

import os
import pytest

from iliad_payment import Card
from iliad_payment import Config
from iliad_payment import Customer
from iliad_payment import Payment
from iliad_payment import Refund
from ..TestHelper import TestHelper


@pytest.mark.skipif(
    os.getenv('API_KEY') is None,
    reason='Require an API key',
)
@pytest.mark.skipif(
    os.getenv('API_HOST') is None,
    reason='Require an API host',
)
class TestFunctionalRefund(TestHelper):
    def setup_method(self, method):
        conf = Config()

        del conf.keys
        conf.keys = str(os.getenv('API_KEY'))
        conf.host = str(os.getenv('API_HOST'))
        conf.timeout = 1

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_single_refund(self, currency):
        amount = self.random_integer(50, 10000)
        desc = 'Refund test, {:.2f} {}'.format(amount / 100, currency.upper())

        card = Card()
        card.number = '4000005780000007'
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.cvc = str(self.random_integer(100, 999))

        customer = Customer()
        customer.name = 'John Doe'
        customer.email = 'john.doe@example.com'

        payment = Payment()

        payment.amount = amount
        payment.card = card
        payment.currency = currency
        payment.customer = customer
        payment.description = desc

        payment.save()

        assert payment.refund() == payment

        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 1
        assert isinstance(refunds[0], Refund)
        assert refunds[0].amount == amount
        assert refunds[0].currency == currency
        assert refunds[0].payment == payment

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_multiple_refund(self, currency):
        amount = self.random_integer(200, 100000)
        refund1 = self.random_integer(50, amount // 4)
        refund2 = self.random_integer(50, amount // 4)
        refund3 = amount - refund1 - refund2
        desc = 'Refund test, {:.2f} {}'.format(amount / 100, currency.upper())

        card = Card()
        card.number = '4000003720000005'
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.cvc = str(self.random_integer(100, 999))

        customer = Customer()
        customer.name = 'John Doe'
        customer.email = 'john.doe@example.com'

        payment = Payment()

        payment.amount = amount
        payment.card = card
        payment.currency = currency
        payment.customer = customer
        payment.description = desc

        payment.save()

        assert payment.refund(refund1) == payment

        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 1
        assert isinstance(refunds[0], Refund)
        assert refunds[0].amount == refund1
        assert refunds[0].currency == currency
        assert refunds[0].payment == payment

        assert payment.refund(refund2) == payment

        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 2

        assert isinstance(refunds[0], Refund)
        assert refunds[0].amount == refund1
        assert refunds[0].currency == currency
        assert refunds[0].payment == payment

        assert isinstance(refunds[1], Refund)
        assert refunds[1].amount == refund2
        assert refunds[1].currency == currency
        assert refunds[1].payment == payment

        assert payment.refund() == payment

        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 3

        assert isinstance(refunds[0], Refund)
        assert refunds[0].amount == refund1
        assert refunds[0].currency == currency
        assert refunds[0].payment == payment

        assert isinstance(refunds[1], Refund)
        assert refunds[1].amount == refund2
        assert refunds[1].currency == currency
        assert refunds[1].payment == payment

        assert isinstance(refunds[2], Refund)
        assert refunds[2].amount == refund3
        assert refunds[2].currency == currency
        assert refunds[2].payment == payment
