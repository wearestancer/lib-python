"""Functional tests for payment intent object"""

import pytest

from stancer import Card
from stancer import PaymentIntent
from stancer import Customer
from stancer.exceptions import NotFoundError
from stancer.exceptions.base import StancerNotImplementedError
from stancer.exceptions.http import ConflictError
from stancer.sepa import Sepa
from stancer.status import ThreedsStatus
from stancer.status.payment_intent import PaymentIntentStatus
from .TestHelper import TestHelper


class TestFunctionalPaymentIntent(TestHelper):
    def test_get(self):
        # 404 with an unknown payment (with a random id)
        with pytest.raises(NotFoundError) as error:
            obj = PaymentIntent(f"pi_{self.random_string(24)}")
            obj.amount

        assert error.value.message == f'Payment intent `{obj.id}` not found'
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404


        # Recover a valid payment
        obj = PaymentIntent('pi_zoiuKRVPoeSUKufHxghJn99T')

        assert obj.amount == 300
        assert obj.currency == 'eur'
        assert set(obj.methods_allowed) == {'sepa','card'}
        assert obj.threeds == ThreedsStatus.REQUIRED
        assert obj.status == PaymentIntentStatus.CAPTURED
        assert obj.capture is True
        assert isinstance(obj.card,Card)
        assert obj.card.id == 'card_XZ8h7vcnEIecJkDdlnI5gyD5'

        assert obj.description is None
        assert obj.metadata is None
        assert obj.order_id is None
        assert obj.return_url is None
        assert obj.url == f'https://payment.stancer.com/test_pi_zoiuKRVPoeSUKufHxghJn99T'


    def test_send_without_methods_patch_method(self):
        amount= 200
        description = 'functional python test send without method'

        payment_intent = PaymentIntent()

        payment_intent.amount = amount
        payment_intent.description = description
        payment_intent.methods_allowed = ['sepa']
        assert payment_intent.send() == payment_intent
        assert payment_intent.id is not None
        assert payment_intent.id.startswith('pi_')
        assert payment_intent.methods_allowed == ['sepa']
        assert payment_intent.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        card = Card()
        card.cvc = '123'
        card.number = '4242424242424242'
        card.exp_month = 12
        card.exp_year =2067

        payment_intent.card = card

        payment_intent.send()

        assert payment_intent.card.id == card.id
        assert payment_intent.status == PaymentIntentStatus.REQUIRE_AUTHENTICATION

        sepa = Sepa('sepa_k6oqETdIVYLU6rH3tbkB1YRW')
        payment_intent.sepa = sepa

        payment_intent.send()

        assert payment_intent.sepa.id == sepa.id
        assert payment_intent.status == PaymentIntentStatus.AUTHORIZED
        assert payment_intent.threeds == ThreedsStatus.REQUIRED
        assert payment_intent.url == f'https://payment.stancer.com/test_{payment_intent.id}'

    def test_send_with_sepa(self):
        amount= 100
        pi= PaymentIntent()
        pi.amount = amount
        pi.methods_allowed=['sepa']
        pi.sepa = Sepa('sepa_k6oqETdIVYLU6rH3tbkB1YRW')
        pi.send()

        assert pi.status == PaymentIntentStatus.PROCESSING

    def test_send_without_patch_with_sepa(self):
        amount= 100
        pi= PaymentIntent()
        pi.amount = amount
        pi.send()
        assert pi.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        pi.sepa = Sepa('sepa_k6oqETdIVYLU6rH3tbkB1YRW')
        pi.send()
        assert pi.status == PaymentIntentStatus.AUTHORIZED

    def test_send_capture(self):
        amount= self.random_integer(50,800)
        pi = PaymentIntent()
        pi.amount = amount
        pi.capture = False
        pi.threeds = 'none'
        pi.send()

        assert pi.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        pi.card=Card('card_nRBHRjo5UP2pLFb27WxApj8l')
        pi.send()

        assert pi.status == PaymentIntentStatus.REQUIRE_AUTHENTICATION

        # For now the only way to test it is to make a payment manually heer
        # I'll work on playwright tests to make it automatic

        with pytest.raises(ConflictError):
            pi.send_capture()

        # assert pi.status == PaymentIntentStatus.CAPTURED

    def test_get_payment(self,version_2):
        pi = PaymentIntent('pi_zoiuKRVPoeSUKufHxghJn99T')
        payments = pi.get_payment_list()
        payment_list =set()
        for payment in payments:
            payment_list.add(payment)
            assert payment.amount == 300
            assert payment.currency =='eur'
        assert len(payment_list) == 1

    def test_complete_crud(self):
        pi = PaymentIntent()
        card = Card()
        card.cvc = '123'
        card.number = '4242424242424242'
        card.exp_month = 11
        card.exp_year = 2090
        customer = Customer()
        customer.email = 'example@stancer.com'
        customer.mobile = self.random_mobile()

        amount = self.random_integer(50,9999)
        capture = True
        currency = 'eur'
        description = 'test complete PI'
        metadata = 'truc'
        methods_allowed = ['card','sepa']
        order_id = 'ID_68'
        return_url = 'https://perdu.com'
        threeds = ThreedsStatus.REQUIRED

        pi.amount = amount
        pi.capture = capture
        pi.card = card
        pi.currency = currency
        pi.customer = customer
        pi.description = description
        pi.metadata = metadata
        pi.methods_allowed = methods_allowed
        pi.order_id = order_id
        pi.return_url = return_url
        pi.threeds = threeds

        assert pi == pi.send()


        assert pi.amount == amount
        assert pi.capture == capture
        assert pi.card.id == card.id
        assert pi.currency == currency
        assert pi.customer.id == customer.id
        assert pi.description == description
        assert pi.metadata == metadata
        assert set(pi.methods_allowed) == set(methods_allowed)
        assert pi.order_id == order_id
        assert pi.return_url == return_url
        assert pi.threeds == threeds
        assert pi.url == f'https://payment.stancer.com/test_{pi.id}'

        #Patch Payment intent
        sepa = Sepa()
        sepa.bic = "TESTFRPP"
        sepa.iban = "FR1420041010050500013M02606"
        sepa.name="Pierre dupont"

        customer2 = Customer()
        customer2.email = f'test{self.random_string(5)}@example.com'
        customer2.mobile = self.random_mobile()
        capture2 = True
        currency2 = 'eur'
        description2 = 'test complete PI'
        metadata2 = 'truc'
        methods_allowed2 = ['card','sepa']
        order_id2 = 'ID_68'
        return_url2 = 'https://perdu.com'
        threeds2 = ThreedsStatus.REQUIRED

        pi.capture = capture2
        pi.sepa = sepa
        pi.currency = currency2
        pi.customer = customer2
        pi.description = description2
        pi.metadata = metadata2
        pi.methods_allowed = methods_allowed2
        pi.order_id = order_id2
        pi.return_url = return_url2
        pi.threeds = threeds2

        pi.send()

        assert pi.capture == capture2
        assert pi.sepa.id == sepa.id
        assert pi.currency == currency2
        assert pi.customer.id == customer2.id
        assert pi.description == description2
        assert pi.metadata == metadata2
        assert set(pi.methods_allowed) == set(methods_allowed2)
        assert pi.order_id == order_id2
        assert pi.return_url == return_url2
        assert pi.threeds == threeds2
        assert pi.url == f'https://payment.stancer.com/test_{pi.id}'

        # DELETE PI This is not possible.

        with pytest.raises(StancerNotImplementedError):
            pi.delete()
