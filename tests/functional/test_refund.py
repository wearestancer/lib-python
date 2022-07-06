"""Functional tests for refunds"""

import pytest

from stancer import Card
from stancer import Customer
from stancer import Payment
from stancer import PaymentStatus
from stancer import Refund
from stancer.exceptions import ConflictError
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

        payment.send()

        assert payment.status == PaymentStatus.TO_CAPTURE

        with pytest.raises(ConflictError) as error:
            payment.refund(amount - 1)

        assert error.value.message == 'Payment cannot be partially refunded before it has been captured'
        assert error.value.reason == 'Conflict'
        assert error.value.status_code == 409

        refund = payment.refund()
        refunds = payment.refunds

        assert isinstance(refund, Refund)
        assert refund.amount == amount
        assert refund.currency == currency
        assert refund.payment == payment

        assert isinstance(refunds, list)
        assert len(refunds) == 1
        assert refunds[0] == refund

        assert payment.status == PaymentStatus.CANCELED

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_multiple_refund(self, currency):
        amount = self.random_integer(200, 100000)
        refund_amount1 = self.random_integer(50, amount // 4)
        refund_amount2 = self.random_integer(50, amount // 4)
        refund_amount3 = amount - refund_amount1 - refund_amount2
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

        payment.send()

        refund1 = payment.refund(refund_amount1)
        refunds = payment.refunds

        assert isinstance(refund1, Refund)
        assert refund1.amount == refund_amount1
        assert refund1.currency == currency
        assert refund1.payment == payment

        assert isinstance(refunds, list)
        assert len(refunds) == 1
        assert refunds[0] == refund1

        refund2 = payment.refund(refund_amount2)
        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 2
        assert refunds[0] == refund1
        assert refunds[1] == refund2

        assert isinstance(refund1, Refund)
        assert refund1.amount == refund_amount1
        assert refund1.currency == currency
        assert refund1.payment == payment

        assert isinstance(refund2, Refund)
        assert refund2.amount == refund_amount2
        assert refund2.currency == currency
        assert refund2.payment == payment

        refund3 = payment.refund()
        refunds = payment.refunds

        assert isinstance(refunds, list)
        assert len(refunds) == 3
        assert refunds[0] == refund1
        assert refunds[1] == refund2
        assert refunds[2] == refund3

        assert isinstance(refund1, Refund)
        assert refund1.amount == refund_amount1
        assert refund1.currency == currency
        assert refund1.payment == payment

        assert isinstance(refund2, Refund)
        assert refund2.amount == refund_amount2
        assert refund2.currency == currency
        assert refund2.payment == payment

        assert isinstance(refund3, Refund)
        assert refund3.amount == refund_amount3
        assert refund3.currency == currency
        assert refund3.payment == payment
