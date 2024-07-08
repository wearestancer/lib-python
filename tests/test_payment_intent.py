# -*- coding: utf-8 -*-

import json
from typing import Generator
from uuid import uuid4

import pytest
import responses

from stancer import Customer, sepa
from stancer import Payment
from stancer import Card
from stancer import PaymentIntent
from stancer import Sepa
from stancer.core import AbstractAmount
from stancer.exceptions import InvalidAmountError
from stancer.exceptions import InvalidCardError
from stancer.exceptions import InvalidCustomerError
from stancer.exceptions import InvalidPaymentIntentCaptureError
from stancer.exceptions import InvalidPaymentIntentDescriptionError
from stancer.exceptions import InvalidPaymentIntentMethodsAllowed
from stancer.exceptions import InvalidPaymentIntentOrderIdError
from stancer.exceptions import InvalidSepaError
from stancer.exceptions import InvalidThreedsStatusError
from stancer.exceptions import InvalidUrlError
from stancer.exceptions import StancerApiVersionError
from stancer.exceptions import StancerNotImplementedError
from stancer.exceptions import StancerValueError
from stancer.exceptions import MissingPaymentIdError
from stancer.exceptions.invalid_value import InvalidSearchFilter
from stancer.status import MethodAllowed
from stancer.status import ThreedsStatus
from stancer.status import PaymentIntentStatus

from .TestHelper import TestHelper


class TestPaymentIntent(TestHelper):

    def test_class(self,version_2):
        assert issubclass(PaymentIntent, AbstractAmount)

    def test_init_api_v1(self,version_1):
        with pytest.raises(StancerApiVersionError):
            PaymentIntent()

    @responses.activate
    def test_amount(self,version_2):
        payment_intent = PaymentIntent()

        assert payment_intent.amount is None

        amount = self.random_integer(50,1000)
        payment_intent.amount = amount

        assert payment_intent.amount is not None
        assert payment_intent.amount == amount

        amount = self.random_integer(0,49)

        with pytest.raises(InvalidAmountError):
            payment_intent.amount = amount

        payment_intent = PaymentIntent(f'pi_{self.random_string(24)}')
        params = {
            'amount': self.random_integer(50, 999999),
        }

        responses.add(
            responses.GET,
            payment_intent.uri,
            json=params
            )
        assert payment_intent.amount == params['amount']
        assert payment_intent.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_capture(self,version_2):
        payment_intent = PaymentIntent()
        capture = True

        assert payment_intent.capture is None

        payment_intent.capture = capture

        assert payment_intent.capture == capture

        with pytest.raises(InvalidPaymentIntentCaptureError):
            payment_intent.capture = self.random_string(12,42)

        payment_intent = PaymentIntent(f'pi_{self.random_string(24)}')
        params = {
            'capture': 'true',
        }

        responses.add(
            responses.GET,
            payment_intent.uri,
            json=params
            )
        assert payment_intent.capture == params['capture']
        assert payment_intent.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_card(self,version_2):
        payment_intent = PaymentIntent()
        card = Card(self.random_integer(29))
        assert payment_intent.card is None

        payment_intent.card = card

        assert payment_intent.card.id == card.id

        with pytest.raises(
            InvalidCardError,
            match= 'You must provide a complete Card.'
        ):
            payment_intent.card = Card()

        with pytest.raises(InvalidCardError):
            payment_intent.card = 'A shrubbery'

        with pytest.raises(InvalidCardError):
            payment_intent.card = self.random_integer(123)

        payment_intent_call = PaymentIntent(self.random_string(29))

        params = {
            'card' : f'card_{self.random_string(24)}'
        }

        responses.add(responses.GET, payment_intent_call.uri, json=params)

        assert isinstance(payment_intent_call.card, Card)
        assert payment_intent_call.card.id == params['card']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize("currency", TestHelper.currency_provider() )
    def test_currency(self,currency,version_2):
        payment_intent = PaymentIntent()
        assert payment_intent.currency is None

        payment_intent.currency = currency


        assert payment_intent.currency is not None

        payment_intent_call = PaymentIntent(self.random_string(29))
        params = {
            'currency' : 'eur'
        }

        responses.add(responses.GET, payment_intent_call.uri, json=params)
        assert payment_intent_call.currency == params['currency']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_customer(self,version_2):
        payment_intent = PaymentIntent()

        assert payment_intent.customer is None

        customer = Customer()
        customer.mobile = self.random_mobile()
        customer.email = 'example@stancer.com'

        params = {
            'id': f'cust_{self.random_string(24)}'
        }
        responses.add(responses.POST, customer.uri, json=params)

        assert len(responses.calls) == 0

        payment_intent.customer = customer

        assert len(responses.calls) == 1

        assert payment_intent.customer.id == customer.id

        with pytest.raises(
            InvalidCustomerError,
            match='You must provide a complete Customer.'
        ):
            payment_intent.customer = Customer()

        with pytest.raises(InvalidCustomerError):
            payment_intent.customer = self.random_integer(64)

        with pytest.raises(InvalidCustomerError):
            payment_intent.customer = self.random_string(34)

        payment_intent_call = PaymentIntent(self.random_string(29))

        params = {
            'customer' : f'cust_{self.random_string(24)}'
        }

        responses.add(responses.GET, payment_intent_call.uri, json=params)

        assert isinstance(payment_intent_call.customer, Customer)
        assert payment_intent_call.customer.id == params['customer']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 2

    def test_delete(self,version_2):
        payment_intent = PaymentIntent()

        with pytest.raises(StancerNotImplementedError):
            payment_intent.delete()

    @responses.activate
    def test_description(self,version_2):
        payment_intent = PaymentIntent()

        assert payment_intent.description is None

        description = self.random_string(3,64)

        payment_intent.description = description

        assert payment_intent.description == description

        with pytest.raises(InvalidPaymentIntentDescriptionError):
            payment_intent.description = self.random_string(0,2)

        with pytest.raises(InvalidPaymentIntentDescriptionError):
            payment_intent.description = self.random_string(65,124)

        with pytest.raises(InvalidPaymentIntentDescriptionError):
            payment_intent.description = self.random_integer(3,64)

        payment_intent_call = PaymentIntent(self.random_string(29))
        params = {
            'description' : 'this is a valid description'
        }
        responses.add(responses.GET, payment_intent_call.uri, json=params)
        assert payment_intent_call.description == params['description']
        assert payment_intent.is_populated
        assert len(responses.calls) == 1

    def test_filter_list_params(self):
        order_id = self.random_string(10)
        card_id = f"card_{self.random_string(24)}"
        sepa_id = f"sepa_{self.random_string(24)}"
        field="created"
        order="asc"

        params = PaymentIntent.filter_list_params(
            order_id=order_id,
            card=card_id,
            sepa=sepa_id,
            field=field,
            order=order,
            )

        assert 'order_id' in params
        assert params['order_id'] == order_id

        assert 'card' in params
        assert params['card'] == card_id

        assert 'sepa' in params
        assert params['sepa'] == sepa_id

        assert 'field' in params
        assert params['field'] == field

        assert 'order' in params
        assert params['order'] == order

        card_obj = Card(f"card_{self.random_string(24)}")
        sepa_obj = Sepa(f"sepa_{self.random_string(24)}")
        params = PaymentIntent.filter_list_params(
            card=card_obj,
            sepa=sepa_obj,
            )

        assert 'card' in params
        assert params['card'] == card_obj.id

        assert 'sepa' in params
        assert params['sepa'] == sepa_obj.id

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid order ID must be between 1 and 36 characters.',
        ):
            PaymentIntent.filter_list_params(order_id='')

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid order ID must be between 1 and 36 characters.',
        ):
            PaymentIntent.filter_list_params(order_id=self.random_string(37))

        with pytest.raises(
            InvalidSearchFilter,
            match='Order ID must be a string.',
        ):
            PaymentIntent.filter_list_params(order_id=self.random_integer(10))

        with pytest.raises(
            InvalidSearchFilter,
            match="Card must be a card ID"
        ):
            PaymentIntent.filter_list_params(card='')

        with pytest.raises(
            InvalidSearchFilter,
            match='Sepa must be a sepa ID',
        ):
            PaymentIntent.filter_list_params(sepa='')

        with pytest.raises(
            InvalidSearchFilter,
            match="Field must be 'created' or 'due'.",
        ):
            PaymentIntent.filter_list_params(field=self.random_integer(10))

        with pytest.raises(
            InvalidSearchFilter,
            match="Field must be 'created' or 'due'.",
        ):
            PaymentIntent.filter_list_params(field='test')

        with pytest.raises(
            InvalidSearchFilter,
            match= "Order must be 'desc' or 'asc'.",
        ):
            PaymentIntent.filter_list_params(order=self.random_integer(10))

        with pytest.raises(
            InvalidSearchFilter,
            match= "Order must be 'desc' or 'asc'.",
        ):
            PaymentIntent.filter_list_params(order="test")


    @responses.activate
    def test_get_payment(self,version_2):
        pi  = PaymentIntent()

        with pytest.raises(MissingPaymentIdError):
            pi.get_payment_list()

        pi = PaymentIntent('bYwva4szr5jN4jx1L9Vezpof')
        list_payment = pi.get_payment_list()

        assert isinstance(list_payment,Generator)

        with open('./tests/fixtures/payment/read.json',) as opened_file:
            params = {
                'payment' : [
                    json.loads(opened_file.read()),
                ],
                'range' :{
                    "start":0,
                    "end":1,
                    "limit":10,
                    "has_more":False,
                }
            }

        responses.add(responses.GET, f'{pi.uri}/payments',json=params)
        for payment in list_payment:
            assert isinstance( payment , Payment)
            assert payment.id == 'paym_SKMLflt8NBATuiUzgvTYqsw5'
            assert payment.amount == 3406
            assert payment.currency == 'eur'

    @responses.activate
    def test_list(self,version_2):
        #we create it just to have a uri for responses add
        pi_uri = PaymentIntent()
        with open('./tests/fixtures/payment_intent/list_payment_intents.json') as opened_file:
            content = opened_file.read()
        responses.add(responses.GET, pi_uri.uri, body=content)
        pi_list = PaymentIntent().list(limit=10)

        first_pi = next(pi_list)
        assert isinstance(first_pi.card, Card)
        assert first_pi.id == "pi_Tn16lAUhI8l3ppgFsiYB6cCs"
        assert first_pi.created_at == 1720443441
        assert first_pi.created is None
        assert first_pi.amount == 583
        assert first_pi.capture is False
        assert first_pi.card.id == "card_nRBHRjo5UP2pLFb27WxApj8l"
        assert first_pi.currency == 'eur'
        assert first_pi.customer is None
        assert first_pi.description is None
        # We test the list as set because we don't want to check for order.
        assert set(first_pi.methods_allowed) == {'card','sepa',}
        assert first_pi.order_id is None
        assert first_pi.sepa is None
        assert first_pi.status == "require_authentication"
        assert first_pi.threeds == "none"
        assert first_pi.url == "https://payment.stancer.com/test_pi_Tn16lAUhI8l3ppgFsiYB6cCs"

        second_pi = next(pi_list)

        assert isinstance(second_pi.sepa, Sepa)
        assert second_pi.id == "pi_Cat0Tp7D7IuiKn477eiLN6nx"
        assert second_pi.created_at == 1720443441
        assert second_pi.created is None
        assert second_pi.amount == 4111
        assert second_pi.capture is True
        assert second_pi.card is None
        assert second_pi.currency == 'eur'
        assert second_pi.customer.id == "cust_7hvOWUeiZE7IKrMjPbjcaUns"
        assert second_pi.description == "test complete PI"
        # We test the list as set because we don't want to check for order.
        assert set(second_pi.methods_allowed) == {'card','sepa',}
        assert second_pi.order_id == "ID_68"
        assert second_pi.return_url == "https://perdu.com"
        assert second_pi.sepa.id == "sepa_GKllAB2Ha9GnVUSBLYWCNWni"
        assert second_pi.status == "authorized"
        assert second_pi.threeds == "required"
        assert second_pi.url == "https://payment.stancer.com/test_pi_Cat0Tp7D7IuiKn477eiLN6nx"

    @responses.activate
    def test_metadata(self,version_2):
        payment_intent = PaymentIntent()
        metadata = self.random_string(999)

        assert payment_intent.metadata is None

        payment_intent.metadata = metadata

        assert payment_intent.metadata == metadata

        payment_intent_call = PaymentIntent(self.random_string(29))
        params = {
            'metadata' : ['card','sepa']
        }

        responses.add(responses.GET, payment_intent_call.uri , json=params)

        assert payment_intent_call.metadata == params['metadata']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_methods_allowed(self,version_2):
        payment_intent = PaymentIntent()
        methods_allowed = [MethodAllowed.CARD]

        assert payment_intent.methods_allowed is None

        payment_intent.methods_allowed = methods_allowed

        assert payment_intent.methods_allowed == methods_allowed
        assert payment_intent.is_modified

        payment_intent2 = PaymentIntent()
        methods_allowed2 = ['apple_pay']

        payment_intent2.methods_allowed = methods_allowed2

        assert payment_intent2.methods_allowed == methods_allowed2

        payment_intent3 = PaymentIntent()
        methods_allowed3 = MethodAllowed.SEPA

        payment_intent3.methods_allowed = methods_allowed3

        assert payment_intent3.methods_allowed == [methods_allowed3]

        with pytest.raises(InvalidPaymentIntentMethodsAllowed):
            payment_intent.methods_allowed = self.random_integer(12)

        with pytest.raises(InvalidPaymentIntentMethodsAllowed):
            payment_intent.methods_allowed = 'android'

        payment_intent_call = PaymentIntent(self.random_string(29))
        params = {
            'methods_allowed' : ['card','sepa']
        }

        responses.add(responses.GET, payment_intent_call.uri , json=params)

        assert payment_intent_call.methods_allowed == params['methods_allowed']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_order_id(self,version_2):
        payment_intent = PaymentIntent()
        order_id = self.random_string(1,36)

        assert payment_intent.order_id is None

        payment_intent.order_id = order_id

        assert payment_intent.order_id == order_id

        uuid= uuid4()
        py = PaymentIntent()
        py.order_id = str(uuid)
        assert py.order_id == str(uuid)

        with pytest.raises(InvalidPaymentIntentOrderIdError):
            payment_intent.order_id = ''

        with pytest.raises(InvalidPaymentIntentOrderIdError):
            payment_intent.order_id = self.random_string(37,64)

        with pytest.raises(InvalidPaymentIntentOrderIdError):
            payment_intent.order_id = self.random_integer(23)

        obj = PaymentIntent(self.random_string(29))
        params = {
            'order_id': self.random_string(1, 36),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.order_id == params['order_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_return_url(self,version_2):
        payment_intent=PaymentIntent()
        return_url = 'https://perdu.com'

        assert payment_intent.return_url is None

        payment_intent.return_url = return_url

        assert payment_intent.return_url == return_url

        with pytest.raises(InvalidUrlError):
            payment_intent.return_url = 'http://www.ismycomputeronfire.com/'

        with pytest.raises(InvalidUrlError):
            payment_intent.return_url = self.random_integer(0,12)

        payment_intent_call = PaymentIntent(self.random_string(29))
        params = {
            'return_url': 'https://truc'
        }

        responses.add(responses.GET, payment_intent_call.uri , json=params)

        assert payment_intent_call.return_url == params['return_url']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_sepa(self,version_2):
        payment_intent = PaymentIntent()
        sepa = Sepa()

        assert payment_intent.sepa is None

        with pytest.raises(
            InvalidSepaError,
            match='You must provide a complete Sepa.'
            ):
            payment_intent.sepa = sepa

        with pytest.raises(
            InvalidSepaError,
            match='You must provide a valid instance of Sepa.',
        ):
            payment_intent.sepa = self.random_integer(2)

        with pytest.raises(
            InvalidSepaError,
            match='You must provide a valid instance of Sepa.',
        ):
            payment_intent.sepa = self.random_string(2)

        sepa.bic = "TESTFRPP"
        sepa.iban = 'FR1420041010050500013M02606'

        params = {
            'sepa': f'sepa_{self.random_string(24)}',
        }

        responses.add(responses.POST, sepa.uri, json=params)

        assert len(responses.calls) == 0

        payment_intent.sepa = sepa

        assert len(responses.calls) == 1

        payment_intent_call = PaymentIntent("sepa_Yqtbqm0gv4Z2yljRJ5hhfugd")

        params = {
            'sepa': f'sepa_{self.random_string(24)}',
        }
        with open('./tests/fixtures/payment_intent/post-with-sepa.json') as opened_file:
            content = opened_file.read()
        responses.add(responses.GET, payment_intent_call.uri, body=content)

        assert isinstance(payment_intent_call.sepa, Sepa)
        assert payment_intent_call.id == "pi_Yqtbqm0gv4Z2yljRJ5hhfugd"
        assert payment_intent_call.created_at == 1717141292
        assert payment_intent_call.created is None
        assert payment_intent_call.amount == 122
        assert payment_intent_call.capture is True
        assert payment_intent_call.card is None
        assert payment_intent_call.currency == 'eur'
        assert payment_intent_call.customer is None
        assert payment_intent_call.description is None
        # We test the list as set because we don't want to check for order.
        assert set(payment_intent_call.methods_allowed) == {'card','sepa',}
        assert payment_intent_call.order_id is None
        assert payment_intent_call.sepa.id == "sepa_Yqtbqm0gv4Z2yljRJ5hhfugd"
        assert len(responses.calls) == 2

    @responses.activate
    def test_status(self,version_2):
        obj = PaymentIntent()
        status = 'invalid_status_for_testing_purpose'

        assert obj.status is None
        with pytest.raises(AttributeError):
            obj.status = status
        # Check with a good status, status cannot be set!
        with pytest.raises(AttributeError):
            obj.status = "require_authentication"


        assert obj.status is None
        obj = PaymentIntent(self.random_string(29))
        params = {
            'status': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.status == params['status']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_send_and_patch(self,version_2):
        payment_intent = PaymentIntent()

        with open('./tests/fixtures/payment_intent/post-amount.json') as opened_file:
            content = opened_file.read()


        # Save response
        responses.add(responses.POST, payment_intent.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            payment_intent.send()

        assert len(responses.calls) == 0

        payment_intent.amount = self.random_integer(50, 999999)

        assert len(responses.calls) == 0

        assert payment_intent.send() == payment_intent

        assert len(responses.calls) == 1
        # Data from fixture
        assert payment_intent.id == 'pi_fIjxmx7WVoRHACoeadtFrUkC'
        assert payment_intent.created_at == 1717080772
        assert payment_intent.created is None
        assert payment_intent.amount == 100
        assert payment_intent.capture is True
        assert payment_intent.card is None
        assert payment_intent.currency == 'eur'
        assert payment_intent.customer is None
        assert payment_intent.description is None
        # We test the list as set because we don't want to check for order.
        assert set(payment_intent.methods_allowed) == {'card','sepa',}
        assert payment_intent.order_id is None
        assert payment_intent.sepa is None

        with open('./tests/fixtures/payment_intent/patch-currency.json') as opened_file:
            content_patch = opened_file.read()
        responses.add(responses.PATCH, payment_intent.uri, body=content_patch)
        payment_intent.currency='usd'
        payment_intent.send()
        assert len(responses.calls) == 2
        # Data from fixture
        assert payment_intent.id == 'pi_fIjxmx7WVoRHACoeadtFrUkC'
        assert payment_intent.created_at == 1717080772
        assert payment_intent.created is None
        assert payment_intent.amount == 100
        assert payment_intent.capture is True
        assert payment_intent.card is None
        assert payment_intent.currency == 'usd'
        assert payment_intent.customer is None
        assert payment_intent.description is None
        # We test the list as set because we don't want to check for order.
        assert set(payment_intent.methods_allowed) == {'card','sepa',}
        assert payment_intent.order_id is None
        assert payment_intent.sepa is None

    @responses.activate
    def test_send_with_card(self,version_2):
        payment_intent = PaymentIntent()
        card = Card()
        card.exp_month = 12
        card.exp_year = 2048
        card.number = '4242424242424242'
        card.cvc = '234'

        with open('./tests/fixtures/card/complete_card.json', encoding='utf-8') as opened_file:
            content_card = opened_file.read()
        responses.add(responses.POST, card.uri, body=content_card)

        assert len(responses.calls) == 0

        payment_intent.card = card

        assert len(responses.calls) == 1

        with open('./tests/fixtures/payment_intent/post-with-card.json', encoding='utf-8') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, payment_intent.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            payment_intent.send()

        assert len(responses.calls) == 1

        payment_intent.amount = self.random_integer(50, 999999)


        assert payment_intent.send() == payment_intent

        assert len(responses.calls) == 2
        # Data from fixture
        assert payment_intent.id == 'pi_Yqtbqm0gv4Z2yljRJ5hhfugd'
        assert payment_intent.created_at == 1717141292
        assert payment_intent.created is None
        assert payment_intent.amount == 122
        assert payment_intent.capture is True
        assert payment_intent.card.id == 'card_oNKkmI6XoRgHxA9HqMOWblfF'
        assert payment_intent.currency == 'eur'
        assert payment_intent.customer is None
        assert payment_intent.description is None
        # We test the list as set because we don't want to check for order.
        assert set(payment_intent.methods_allowed) == {'card','sepa',}
        assert payment_intent.order_id is None
        assert payment_intent.sepa is None

    @responses.activate
    def test_threeds(self,version_2):
        payment_intent = PaymentIntent()
        threeds = ThreedsStatus.NONE

        assert payment_intent.threeds is None

        payment_intent.threeds = threeds

        assert payment_intent.threeds == threeds

        threeds = 'none'

        payment_intent.threeds = threeds

        assert payment_intent.threeds == threeds

        with pytest.raises(InvalidThreedsStatusError):
            payment_intent.threeds = self.random_integer(789)

        # We must test for a bad string, that isn't back by the Threeds Enum.
        # That doesn't exist for now.

        payment_intent_call = PaymentIntent(self.random_string(29))

        params = {
            'threeds': 'required',
        }

        responses.add(responses.GET, payment_intent_call.uri, json=params)

        assert payment_intent_call.threeds == params['threeds']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    def test_uri(self, version_2):
        payment_intent = PaymentIntent()
        uid = self.random_string(29)

        config_version = self.api_version()
        config_host = self.conf.host
        assert payment_intent.uri == f'https://{config_host}/v{config_version}/payment_intents/'

        payment_intent.hydrate(id=uid)

        assert payment_intent.uri == f'https://api.stancer.com/v{config_version}/payment_intents/{uid}'

    @responses.activate
    def test_url(self, version_2):
        pi = PaymentIntent()

        assert pi.url is None

        with pytest.raises(AttributeError):
            pi.url = "test"
        with pytest.raises(AttributeError):
            pi.url = "http://test"

        payment_intent_call = PaymentIntent(self.random_string(29))

        params = {
            'url': 'https://payment_page.stancer.com',
        }

        responses.add(responses.GET, payment_intent_call.uri, json=params)

        assert payment_intent_call.url == params['url']
        assert payment_intent_call.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_send_capture(self, version_2):
        pi= PaymentIntent()

        with pytest.raises(StancerValueError):
            pi.send_capture()

        del pi
        pi = PaymentIntent(f'pi_{self.random_string(24)}')

        paramstatus= {
            "status": str(PaymentIntentStatus.AUTHORIZED)
        }
        responses.add(responses.GET,pi.uri,json=paramstatus)
        assert pi.status == PaymentIntentStatus.AUTHORIZED

        params={
            "status": str(PaymentIntentStatus.CAPTURED)
        }
        responses.add(responses.POST,f'{pi.uri}/capture',json=params)

        pi.send_capture()
        assert pi.status == PaymentIntentStatus.CAPTURED
