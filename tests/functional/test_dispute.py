"""Functional tests for payment object"""

from time import time

from iliad_payment import Card
from iliad_payment import Dispute
from iliad_payment import Payment
from .TestHelper import TestHelper


class TestFunctionalDispute(TestHelper):
    def test_list(self):
        amount = self.random_integer(50, 100_00)
        currency = TestHelper.currency_provider(True)

        payment = Payment()
        payment.amount = amount
        payment.currency = currency
        payment.description = 'Automatic test for disputes list, {} {}'.format(amount / 100, currency.upper())

        payment.card = Card()
        payment.card.number = self.get_disputed_card_number()
        payment.card.exp_month = self.random_integer(1, 12)
        payment.card.exp_year = self.random_year()
        payment.card.cvc = str(self.random_integer(100, 999))

        payment.send()

        created = int(time()) - 10
        counter = 0

        for dispute in Dispute.list(created=created):
            assert isinstance(dispute, Dispute)
            assert isinstance(dispute.payment, Payment)
            assert dispute.payment.id == payment.id

            counter += 1

        assert counter == 1
