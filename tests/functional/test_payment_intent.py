"""Functional tests for payment intent object"""

import pytest

from stancer import Card
from stancer import Customer
from stancer import PaymentIntent
from stancer.core.enum.version import Version
from stancer.exceptions import NotFoundError
from stancer.exceptions.base import StancerNotImplementedError
from stancer.exceptions.http import ConflictError
from stancer.sepa import Sepa
from stancer.status import ThreedsStatus
from stancer.status.payment_intent import PaymentIntentStatus

from .FunctionalTestHelper import FunctionalTestHelper


class TestFunctionalPaymentIntent(FunctionalTestHelper):
    def test_get(self, version=Version.API_V2):
        self.conf.version = version
        # 404 with an unknown payment (with a random id)
        with pytest.raises(NotFoundError) as error:
            obj = PaymentIntent(f'pi_{self.random_string(24)}')
            obj.amount

        assert error.value.message == f'Payment intent `{obj.id}` not found'
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404

        # Recover a valid payment
        obj = PaymentIntent('pi_dm033KXVAXflbzjv9MQ4Ndyh')

        assert obj.amount == 2700
        assert obj.currency == 'eur'
        assert set(obj.methods_allowed) == {'sepa', 'card'}
        assert obj.threeds == ThreedsStatus.REQUIRED
        assert obj.status == PaymentIntentStatus.CAPTURED
        assert obj.capture is True
        assert isinstance(obj.card, Card)
        assert obj.card.id == 'card_si9kF0BO5ALWjzVIb9GpShaS'
        assert isinstance(obj.customer, Customer)
        assert obj.customer.id == 'cust_WfmZH45DXEi7w3GRgDBGWBt9'

        assert obj.description == 'test complete PI'
        assert obj.metadata is None
        assert obj.order_id == 'ID_qTOpXGDpvvidjePpcLOEfXCBdycUvfTQu'
        assert obj.return_url == 'https://free.fr'
        host = self.conf.host.replace('api.', 'payment.')
        assert obj.url == f'https://{host}/test_pi_dm033KXVAXflbzjv9MQ4Ndyh'

    def test_send_without_methods_patch_method(self, version=Version.API_V2):
        self.conf.version = version
        amount = 200
        description = 'functional python test send without method'

        payment_intent = PaymentIntent()

        payment_intent.amount = amount
        payment_intent.description = description
        assert payment_intent.send() == payment_intent
        assert payment_intent.id is not None
        assert payment_intent.id.startswith('pi_')
        assert payment_intent.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        card = Card()
        card.cvc = '123'
        card.number = '4242424242424242'
        card.exp_month = 12
        card.exp_year = 2067

        payment_intent.card = card

        payment_intent.send()

        assert payment_intent.card.id == card.id
        assert payment_intent.status == PaymentIntentStatus.REQUIRE_AUTHENTICATION

        sepa = Sepa('sepa_gRet9wI8K6dxyaCzzic6Br1t')
        payment_intent.sepa = sepa

        payment_intent.send()

        assert payment_intent.sepa.id == sepa.id
        assert payment_intent.status == PaymentIntentStatus.AUTHORIZED
        assert payment_intent.threeds == ThreedsStatus.REQUIRED
        host = self.conf.host.replace('api.', 'payment.')
        assert payment_intent.url == f'https://{host}/test_{payment_intent.id}'

    def test_send_with_sepa(self, version=Version.API_V2):
        self.conf.version = version
        amount = 100
        pi = PaymentIntent()
        pi.amount = amount
        pi.methods_allowed = ['sepa']
        pi.sepa = Sepa('sepa_gRet9wI8K6dxyaCzzic6Br1t')
        pi.send()

        assert pi.status == PaymentIntentStatus.PROCESSING

    def test_send_without_patch_with_sepa(self, version=Version.API_V2):
        self.conf.version = version
        amount = 100
        pi = PaymentIntent()
        pi.amount = amount
        pi.send()
        assert pi.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        pi.sepa = Sepa('sepa_gRet9wI8K6dxyaCzzic6Br1t')
        pi.send()
        assert pi.status == PaymentIntentStatus.AUTHORIZED

    def test_send_capture(self, version=Version.API_V2):
        self.conf.version = version
        amount = self.random_integer(50, 800)
        pi = PaymentIntent()
        pi.amount = amount
        pi.capture = False
        pi.threeds = 'none'
        pi.send()

        assert pi.status == PaymentIntentStatus.REQUIRE_PAYMENT_METHOD

        pi.card = Card('card_si9kF0BO5ALWjzVIb9GpShaS')
        pi.send()

        assert pi.status == PaymentIntentStatus.REQUIRE_AUTHENTICATION

        with pytest.raises(ConflictError):
            pi.send_capture()

    def test_get_payment(self, version=Version.API_V2):
        self.conf.version = version
        pi = PaymentIntent('pi_4BtRpGvmKYWYR1XsUhVglmyG')
        payments = pi.get_payment_list()
        payment_list = set()
        for payment in payments:
            payment_list.add(payment)
            assert payment.amount == 8883
            assert payment.currency == 'eur'
        assert len(payment_list) == 1

    def test_complete_crud(self, version=Version.API_V2):
        self.conf.version = version
        pi = PaymentIntent()
        card = Card()
        card.cvc = '123'
        card.number = '4242424242424242'
        card.exp_month = 11
        card.exp_year = 2090
        customer = Customer()
        customer.name = 'John Doe'
        customer.email = f'john_doe+{self.random_string(12)}@stancer.com'
        customer.mobile = self.random_mobile()

        amount = self.random_integer(50, 9999)
        capture = False
        currency = 'eur'
        description = 'test complete PI'
        metadata = self.random_string(60)
        methods_allowed = ['card', 'sepa']
        order_id = f'ID_{self.random_string(33)}'
        return_url = 'https://free.fr'
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
        clean_pi = PaymentIntent(pi.id)

        assert clean_pi.amount == amount
        assert clean_pi.capture == capture
        assert clean_pi.card.id == card.id
        assert clean_pi.currency == currency
        assert clean_pi.customer.id == customer.id
        assert clean_pi.description == description
        assert set(clean_pi.methods_allowed) == set(methods_allowed)
        assert clean_pi.order_id == order_id
        assert clean_pi.return_url == return_url
        assert clean_pi.threeds == threeds
        host = self.conf.host.replace('api.', 'payment.')
        assert clean_pi.url == f'https://{host}/test_{pi.id}'

        # Patch Payment intent
        sepa = Sepa()
        sepa.bic = 'TESTFRPP'
        sepa.iban = 'FR1420041010050500013M02606'
        sepa.name = 'Pierre dupont'

        customer2 = Customer()
        customer2.email = f'test{self.random_string(5)}@example.com'
        customer2.mobile = self.random_mobile()
        capture2 = True
        currency2 = 'eur'
        description2 = 'test complete PI'
        metadata2 = 'truc'
        methods_allowed2 = ['card', 'sepa']
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
        host = self.conf.host.replace('api.', 'payment.')
        assert pi.url == f'https://{host}/test_{pi.id}'

        # Deleting Payment Intent is not possible.

        with pytest.raises(StancerNotImplementedError):
            pi.delete()

    def test_list(self, version=Version.API_V2):
        self.conf.version = version
        pi_list = PaymentIntent().list(
            card='card_si9kF0BO5ALWjzVIb9GpShaS', order='asc'
        )

        first_pi = next(pi_list)
        assert isinstance(first_pi.card, Card)
        assert first_pi.id == 'pi_lydVCyMTK9HNgK4dGyC4Yb9x'
        assert first_pi.created_at == 1759853014
        assert first_pi.created is None
        assert first_pi.amount == 5912
        assert first_pi.capture is False
        assert first_pi.card.id == 'card_si9kF0BO5ALWjzVIb9GpShaS'
        assert first_pi.currency == 'eur'
        assert first_pi.customer.id == 'cust_x1cUjSpENH0KjexWh113izqc'
        assert first_pi.description == 'test complete PI'
        # We test the list as set because we don't want to check for order.
        assert set(first_pi.methods_allowed) == {
            'card',
            'sepa',
        }
        assert first_pi.order_id == 'ID_68'
        assert first_pi.sepa is None
        assert first_pi.status == PaymentIntentStatus.AUTHORIZED
        assert first_pi.threeds == ThreedsStatus.REQUIRED
        host = self.conf.host.replace('api.', 'payment.')
        assert first_pi.url == f'https://{host}/test_pi_lydVCyMTK9HNgK4dGyC4Yb9x'

        second_pi = next(pi_list)
        assert isinstance(second_pi.card, Card)
        assert second_pi.id == 'pi_4BtRpGvmKYWYR1XsUhVglmyG'
        assert second_pi.created_at == 1759913918
        assert second_pi.created is None
        assert second_pi.amount == 8883
        assert second_pi.capture is False
        assert second_pi.card.id == 'card_si9kF0BO5ALWjzVIb9GpShaS'
        assert second_pi.currency == 'eur'
        assert second_pi.customer.id == 'cust_kwa92KhGYavE0FP8nMlF4I4g'
        assert second_pi.description == 'test complete PI'
        # We test the list as set because we don't want to check for order.
        assert set(second_pi.methods_allowed) == {
            'card',
            'sepa',
        }
        assert second_pi.order_id == 'ID_kiQqHxGtugdSFWKKJD5LxvkgeT3rr4lOj'
        assert second_pi.return_url == 'https://free.fr'
        assert second_pi.sepa is None
        assert second_pi.status == PaymentIntentStatus.AUTHORIZED
        assert second_pi.threeds == ThreedsStatus.REQUIRED
        host = self.conf.host.replace('api.', 'payment.')
        assert second_pi.url == f'https://{host}/test_pi_4BtRpGvmKYWYR1XsUhVglmyG'
