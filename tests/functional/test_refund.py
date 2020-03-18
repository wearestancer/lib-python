"""Functional tests for refunds"""

import pytest

from iliad_payment import Card
from iliad_payment import Customer
from iliad_payment import Payment
from iliad_payment import PaymentStatus
from iliad_payment import Refund
from iliad_payment.exceptions import ConflictError
from .TestHelper import TestHelper


class TestFunctionalRefund(TestHelper):
    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_single_refund(self, currency):
        amount = self.random_integer(100, 10000)
        desc = 'Refund test, {:.2f} {}'.format(amount / 100, currency.upper())

        card = Card()
        card.number = self.get_card_number()
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

        assert payment.status == PaymentStatus.TO_CAPTURE

        with pytest.raises(ConflictError) as error:
            payment.refund(amount - 1)

        assert error.value.status_code == 409
        assert error.value.reason == 'Conflict'
        assert error.value.message['error'] == 'Payment cannot be partially refunded before it has been captured'

        assert payment.refund() == payment

        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 1
        assert isinstance(refunds[0], Refund)
        assert refunds[0].amount == amount
        assert refunds[0].currency == currency
        assert refunds[0].payment == payment

        assert payment.status == PaymentStatus.CANCELED

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_multiple_refund(self, currency):
        amount = self.random_integer(200, 100000)
        refund1 = self.random_integer(50, amount // 4)
        refund2 = self.random_integer(50, amount // 4)
        refund3 = amount - refund1 - refund2
        desc = 'Refund test, {:.2f} {}'.format(amount / 100, currency.upper())

        card = Card()
        card.number = '4000000000000077'
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
