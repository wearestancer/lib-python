"""Test payment object"""

import json
import uuid

from datetime import date
from datetime import datetime
from datetime import timezone
from datetime import tzinfo

import pytest
import responses

from pytz import timezone as tz

from stancer.auth import Auth
from stancer.card import Card
from stancer.config import Config
from stancer.core.abstract_amount import AbstractAmount
from stancer.core.abstract_country import AbstractCountry
from stancer.core.abstract_object import AbstractObject
from stancer.core.abstract_search import AbstractSearch
from stancer.core.enum.version import Version
from stancer.core.payment.auth import PaymentAuth
from stancer.core.payment.page import PaymentPage
from stancer.core.payment.refund import PaymentRefund
from stancer.customer import Customer
from stancer.device import Device
from stancer.exceptions import InvalidAmountError
from stancer.exceptions import InvalidAuthError
from stancer.exceptions import InvalidCardError
from stancer.exceptions import InvalidCurrencyError
from stancer.exceptions import InvalidCustomerError
from stancer.exceptions import InvalidDeviceError
from stancer.exceptions import InvalidIpAddressError
from stancer.exceptions import InvalidPaymentCaptureError
from stancer.exceptions import InvalidPaymentDescriptionError
from stancer.exceptions import InvalidPaymentOrderIdError
from stancer.exceptions import InvalidPaymentUniqueIdError
from stancer.exceptions import InvalidPortError
from stancer.exceptions import InvalidSearchFilter
from stancer.exceptions import InvalidSepaError
from stancer.exceptions import InvalidStatusError
from stancer.exceptions import InvalidUrlError
from stancer.exceptions import MissingApiKeyError
from stancer.exceptions import MissingPaymentIdError
from stancer.exceptions import MissingPaymentMethodError
from stancer.exceptions import MissingReturnUrlError
from stancer.exceptions import StancerNotImplementedError
from stancer.payment import Payment
from stancer.refund import Refund
from stancer.sepa import Sepa
from stancer.status.auth import AuthStatus
from stancer.status.payment import PaymentStatus
from stancer.status.refund import RefundStatus

from .TestHelper import TestHelper


class TestPayment(TestHelper):
    # region mixed
    def test_class(self):
        assert issubclass(Payment, AbstractAmount)
        assert issubclass(Payment, AbstractCountry)
        assert issubclass(Payment, AbstractObject)
        assert issubclass(Payment, AbstractSearch)
        assert issubclass(Payment, PaymentAuth)
        assert issubclass(Payment, PaymentPage)
        assert issubclass(Payment, PaymentRefund)

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_amount(self, version):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag and auto population
        self.conf.version = version
        obj = Payment()
        amount = self.random_integer(50, 999999)

        assert obj.is_not_modified

        obj.amount = amount

        assert obj.amount == amount
        assert obj.is_modified

        obj = Payment(self.random_string(29))
        params = {
            'amount': self.random_integer(50, 999999),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.amount == params['amount']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_capture(self, version):
        self.conf.version = version
        obj = Payment()

        assert obj.capture is None
        assert obj.is_not_modified

        obj.capture = True
        assert obj.capture is True
        assert obj.is_modified

        obj.capture = False
        assert obj.capture is False

        with pytest.raises(
            InvalidPaymentCaptureError,
            match='Capture must be a boolean',
        ):
            obj.capture = self.random_integer(2)

        with pytest.raises(
            InvalidPaymentCaptureError,
            match='Capture must be a boolean',
        ):
            obj.capture = self.random_string(2)

        obj = Payment(self.random_string(29))
        params = {
            'capture': True,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.capture == params['capture']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_card(self, version):
        self.conf.version = version
        obj = Payment()
        card = Card()

        assert obj.card is None
        assert obj.method is None

        obj.card = card

        assert obj.card == card
        assert obj.method == 'card'

        with pytest.raises(
            InvalidCardError,
            match='You must provide a valid instance of Card',
        ):
            obj.card = self.random_integer(2)

        with pytest.raises(
            InvalidCardError,
            match='You must provide a valid instance of Card',
        ):
            obj.card = self.random_string(2)

        obj = Payment(self.random_string(29))

        params = {
            'card': self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.card, Card)
        assert obj.card.id == params['card']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_customer(self, version):
        self.conf.version = version
        obj = Payment()
        customer = Customer()

        assert obj.customer is None

        obj.customer = customer

        assert obj.customer == customer

        with pytest.raises(
            InvalidCustomerError,
            match='You must provide a valid instance of Customer.',
        ):
            obj.customer = self.random_integer(2)

        with pytest.raises(
            InvalidCustomerError,
            match='You must provide a valid instance of Customer.',
        ):
            obj.customer = self.random_string(2)

        obj = Payment(self.random_string(29))

        params = {
            'customer': self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.customer, Customer)
        assert obj.customer.id == params['customer']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_date_bank(self, version):
        self.conf.version = version
        obj = Payment()
        config = Config()
        zone = 'Europe/Paris'
        timestamp = self.random_integer(1500000000, 1600000000)

        assert obj.date_bank is None

        params = {
            'date_bank': timestamp,
        }

        obj.hydrate(**params)

        assert isinstance(obj.date_bank, datetime)
        assert obj.date_bank.timestamp() == timestamp
        assert obj.date_bank.tzinfo is timezone.utc

        config.default_timezone = tz(zone)

        obj.hydrate(**params)

        assert isinstance(obj.date_bank, datetime)
        assert obj.date_bank.timestamp() == timestamp
        assert isinstance(obj.date_bank.tzinfo, tzinfo)
        assert obj.date_bank.tzinfo.zone == zone

        obj = Payment(self.random_string(29))
        params = {
            'date_bank': self.random_integer(1500000000, 1600000000),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.date_bank, datetime)
        assert obj.date_bank.timestamp() == params['date_bank']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_description(self, version):
        self.conf.version = version
        obj = Payment()
        description = self.random_string(3, 64)

        assert obj.description is None

        obj.description = description

        assert obj.description == description

        with pytest.raises(
            InvalidPaymentDescriptionError,
            match='Description must be a string.',
        ):
            obj.description = self.random_integer(20)

        with pytest.raises(
            InvalidPaymentDescriptionError,
            match='Description must be between 3 and 64 characters.',
        ):
            obj.description = self.random_string(2)

        with pytest.raises(
            InvalidPaymentDescriptionError,
            match='Description must be between 3 and 64 characters.',
        ):
            obj.description = self.random_string(65)

        obj = Payment(self.random_string(29))
        params = {
            'description': self.random_string(3, 64),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.description == params['description']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_delete(self, version):
        self.conf.version = version
        obj = Payment(self.random_string(29))

        with pytest.raises(
            StancerNotImplementedError,
            match=(
                'You are not allowed to delete a payment, '
                'you need to refund it instead.'
            ),
        ):
            obj.delete()

    @responses.activate
    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_currency(self, currency, version):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag and auto population
        self.conf.version = version
        obj = Payment()

        assert obj.is_not_modified

        obj.currency = currency

        assert obj.currency == currency
        assert obj.is_modified

        obj = Payment(self.random_string(29))
        params = {
            'currency': currency,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.currency == params['currency']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_device(self, version):
        self.conf.version = version
        obj = Payment()
        device = Device()

        assert obj.device is None

        obj.device = device

        assert obj.device == device

        with pytest.raises(
            InvalidDeviceError,
            match='You must provide a valid instance of Device',
        ):
            obj.device = self.random_integer(2)

        with pytest.raises(
            InvalidDeviceError,
            match='You must provide a valid instance of Device',
        ):
            obj.device = self.random_string(2)

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_fee(self, version):
        self.conf.version = version
        obj = Payment()

        assert obj.fee is None

        with pytest.raises(AttributeError):
            obj.fee = self.random_integer(1, 50)

        obj = Payment(self.random_string(29))
        params = {
            'fee': self.random_integer(1, 50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.fee == params['fee']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_filter_list_params(self, version):
        self.conf.version = version
        order_id = self.random_string(10)
        unique_id = self.random_string(10)

        params = Payment.filter_list_params(order_id=order_id, unique_id=unique_id)

        assert 'order_id' in params
        assert params['order_id'] == order_id

        assert 'unique_id' in params
        assert params['unique_id'] == unique_id

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid order ID must be between 1 and 36 characters.',
        ):
            Payment.filter_list_params(order_id='')

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid order ID must be between 1 and 36 characters.',
        ):
            Payment.filter_list_params(order_id=self.random_string(37))

        with pytest.raises(
            InvalidSearchFilter,
            match='Order ID must be a string.',
        ):
            Payment.filter_list_params(order_id=self.random_integer(10))

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid unique ID must be between 1 and 36 characters.',
        ):
            Payment.filter_list_params(unique_id='')

        with pytest.raises(
            InvalidSearchFilter,
            match='A valid unique ID must be between 1 and 36 characters.',
        ):
            Payment.filter_list_params(unique_id=self.random_string(37))

        with pytest.raises(
            InvalidSearchFilter,
            match='Unique ID must be a string.',
        ):
            Payment.filter_list_params(unique_id=self.random_integer(10))

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_hydrate(self, version):
        self.conf.version = version
        obj = Payment()

        params = {
            'card': {},
            'customer': {},
            'sepa': {},
        }

        assert obj.hydrate(**params) == obj

        assert obj.card is None
        assert obj.customer is None
        assert obj.sepa is None

        params = {
            'card': self.random_string(29),
            'customer': self.random_string(29),
            'sepa': self.random_string(29),
        }

        assert obj.hydrate(**params) == obj

        assert isinstance(obj.card, Card)
        assert obj.card.id == params['card']

        assert isinstance(obj.customer, Customer)
        assert obj.customer.id == params['customer']

        assert isinstance(obj.sepa, Sepa)
        assert obj.sepa.id == params['sepa']

        params = {
            'refunds': [
                {
                    'amount': self.random_integer(100, 10000),
                    'currency': 'eur',
                    'status': RefundStatus.TO_REFUND,
                },
            ],
        }

        assert obj.hydrate(**params) == obj

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 1

        refund = obj.refunds[0]

        assert isinstance(refund, Refund)
        assert refund.amount == params['refunds'][0]['amount']
        assert refund.currency == params['refunds'][0]['currency']
        assert refund.status == params['refunds'][0]['status']

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_is_success(self, version):
        self.conf.version = version
        obj = Payment()

        # Both false if undefined

        assert obj.is_success is False
        assert obj.is_error is False

        assert obj.is_not_success is True
        assert obj.is_not_error is True

        # Captured payments are success

        obj.hydrate(status=PaymentStatus.CAPTURED)

        assert obj.is_success is True
        assert obj.is_error is False

        assert obj.is_not_success is False
        assert obj.is_not_error is True

        # Awaiting for capture payments are success

        obj.hydrate(status=PaymentStatus.TO_CAPTURE)

        assert obj.is_success is True
        assert obj.is_error is False

        assert obj.is_not_success is False
        assert obj.is_not_error is True

        # Authorized payments not asked for capture are success

        obj.hydrate(capture=False, status=PaymentStatus.AUTHORIZED)

        assert obj.is_success is True
        assert obj.is_error is False

        assert obj.is_not_success is False
        assert obj.is_not_error is True

        # Authorized payments asked for capture are error

        obj.hydrate(capture=True, status=PaymentStatus.AUTHORIZED)

        assert obj.is_success is False
        assert obj.is_error is True

        assert obj.is_not_success is True
        assert obj.is_not_error is False

        # Others are all errors

        statuses = [
            PaymentStatus.CANCELED,
            PaymentStatus.DISPUTED,
            PaymentStatus.EXPIRED,
            PaymentStatus.FAILED,
        ]

        for status in statuses:
            obj.hydrate(status=status)

            assert obj.is_success is False
            assert obj.is_error is True

            assert obj.is_not_success is True
            assert obj.is_not_error is False

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_method(self, version):
        self.conf.version = version
        obj = Payment()

        assert obj.method is None

        with pytest.raises(AttributeError):
            obj.method = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'method': self.random_string(4),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.method == params['method']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_order_id(self, version):
        self.conf.version = version
        obj = Payment()
        order_id = self.random_string(1, 36)

        assert obj.order_id is None

        obj.order_id = order_id

        assert obj.order_id == order_id

        with pytest.raises(
            InvalidPaymentOrderIdError,
            match='Order id must be a string.',
        ):
            obj.order_id = self.random_integer(20)

        with pytest.raises(
            InvalidPaymentOrderIdError,
            match='Order id must be 36 characters maximum.',
        ):
            obj.order_id = self.random_string(37, 50)

        obj = Payment(self.random_string(29))
        params = {
            'order_id': self.random_string(1, 36),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.order_id == params['order_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

        # Works with uuid

        obj = Payment()
        order_id = uuid.uuid4()

        assert obj.order_id is None

        obj.order_id = order_id

        assert obj.order_id == str(order_id)

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_refund(self, version):
        self.conf.version = version
        with open('./tests/fixtures/payment/read-no-card.json') as opened_file:
            payment_content = json.load(opened_file)

        with open('./tests/fixtures/refund/read.json') as opened_file:
            refund1_content = json.load(opened_file)

        with open('./tests/fixtures/refund/read.json') as opened_file:
            refund2_content = json.load(opened_file)

        obj = Payment(payment_content['id'])

        paid = payment_content['amount']

        refund1_amount = self.random_integer(50, paid - 50)
        refund1_content['amount'] = refund1_amount
        ref = Refund()

        refund2_amount = paid - refund1_amount
        refund2_content['amount'] = refund2_amount
        refund2_content['id'] = f'refd_{self.random_string(24)}'

        responses.reset()
        responses.add(responses.GET, obj.uri, json=payment_content)
        responses.add(responses.POST, ref.uri, json=refund1_content)
        responses.add(responses.POST, ref.uri, json=refund2_content)

        assert isinstance(obj.refunds, list)
        assert not len(obj.refunds)
        assert len(responses.calls) == 1

        refund1 = obj.refund(refund1_amount)

        assert isinstance(refund1, Refund)
        assert len(responses.calls) == 2

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 1
        assert refund1.id == refund1_content['id']
        assert refund1.amount == refund1_amount
        assert obj.refunds[0] == refund1

        with pytest.raises(InvalidAmountError) as err:
            obj.refund(paid)

        assert str(err.value) == (
            f'You are trying to refund ({paid / 100:.2f} {obj.currency.upper()}) more than possible '
            f'({refund2_amount / 100:.2f} {obj.currency.upper()}).'
        )
        refund2 = obj.refund()

        assert isinstance(refund2, Refund)
        assert len(responses.calls) == 3

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 2
        assert refund1.id == refund1_content['id']
        assert refund1.amount == refund1_amount
        assert refund2.id == refund2_content['id']
        assert refund2.amount == refund2_amount
        assert obj.refunds[0] == refund1
        assert obj.refunds[1] == refund2

        assert obj.is_not_modified

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_refundable_amount(self, version):
        self.conf.version = version
        with open('./tests/fixtures/payment/read.json') as opened_file:
            payment_content = json.load(opened_file)

        with open('./tests/fixtures/refund/read.json') as opened_file:
            refund_content = json.load(opened_file)

        obj = Payment(payment_content['id'])

        paid = payment_content['amount']

        refund_amount = self.random_integer(50, paid - 50)
        refund_content['amount'] = refund_amount
        ref = Refund()

        responses.reset()
        responses.add(responses.GET, obj.uri, json=payment_content)
        responses.add(responses.POST, ref.uri, json=refund_content)

        assert obj.refundable_amount == obj.amount

        obj.refund(refund_amount)

        assert obj.refundable_amount == paid - refund_amount

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_refunded_amount(self, version):
        self.conf.version = version
        with open('./tests/fixtures/payment/read.json') as opened_file:
            payment_content = json.load(opened_file)

        with open('./tests/fixtures/refund/read.json') as opened_file:
            refund_content = json.load(opened_file)

        obj = Payment(payment_content['id'])

        paid = payment_content['amount']

        refund_amount = self.random_integer(50, paid - 50)
        refund_content['amount'] = refund_amount
        ref = Refund()

        responses.reset()
        responses.add(responses.GET, obj.uri, json=payment_content)
        responses.add(responses.POST, ref.uri, json=refund_content)

        assert obj.refunded_amount == 0

        obj.refund(refund_amount)

        assert obj.refunded_amount == refund_amount

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_response(self, version):
        self.conf.version = version
        obj = Payment()

        assert obj.response is None

        with pytest.raises(AttributeError):
            obj.response = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'response': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.response == params['response']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_response_message(self, version):
        self.conf.version = version
        obj = Payment()

        assert obj.response_message is None

        with pytest.raises(AttributeError):
            obj.response_message = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'response': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.response == params['response']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_return_url(self, version):
        self.conf.version = version
        obj = Payment()
        return_url = f'https://www.example.org/?{self.random_string(20)}'

        assert obj.return_url is None

        obj.return_url = return_url

        assert obj.return_url == return_url

        with pytest.raises(
            InvalidUrlError,
            match='Return URL must be a string.',
        ):
            obj.return_url = self.random_integer(20)

        with pytest.raises(
            InvalidUrlError,
            match='Return URL must use HTTPS protocol.',
        ):
            obj.return_url = f'http://www.example.org/?{self.random_string(20)}'

        obj = Payment(self.random_string(29))
        params = {'return_url': f'https://www.example.org/?{self.random_string(20)}'}

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.return_url == params['return_url']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_payment_page_url(self, version):
        self.conf.version = version
        obj = Payment(
            amount=self.random_integer(50, 99999), currency=self.currency_provider(True)
        )

        return_url = 'https://www.example.org/?' + self.random_string(10)

        with open('./tests/fixtures/payment/create-no-method-auth.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with pytest.raises(
            MissingReturnUrlError,
            match='You must provide a return URL before going to the payment page.',
        ):
            obj.payment_page_url()

        obj.return_url = return_url

        with pytest.raises(
            MissingPaymentIdError,
            match='A payment ID is mandatory to obtain a payment page URL. Maybe you forgot to send the payment.',
        ):
            obj.payment_page_url()

        obj.send()
        with pytest.raises(
            MissingApiKeyError,
            match='A public API key is needed to obtain a payment page URL.',
        ):
            obj.payment_page_url()

        config = Config()
        config.version = version
        config.keys = 'ptest_' + self.random_string(24)

        host = config.host.replace('api', 'payment')

        url = f'https://{host}/{config.ptest}/{obj.id}'

        assert obj.payment_page_url() == url

        # With lang parameter
        lang = self.random_string(10)
        url = f'https://{host}/{config.ptest}/{obj.id}?lang={lang}'

        assert obj.payment_page_url(lang=lang) == url

        # With bad parameter (ignored)
        url = f'https://{host}/{config.ptest}/{obj.id}'

        assert obj.payment_page_url(unknown=lang) == url

        # With a port
        config.port = self.random_integer(1000, 65535)
        url = f'https://{host}:{config.port}/{config.ptest}/{obj.id}'

        assert obj.payment_page_url() == url

        # With non ascii chars
        input = self.random_string(2) + ' ' + self.random_string(2)
        encoded = input.replace(' ', '+')
        url = f'https://{host}:{config.port}/{config.ptest}/{obj.id}?lang={encoded}'

        assert obj.payment_page_url(lang=input) == url

        del config.keys
        del config.port

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_send_with_auth_for_payment_page(self, monkeypatch, version):
        self.conf.version = version
        obj = Payment()

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        port = self.random_integer(1, 65535)

        obj.auth = True

        monkeypatch.setenv('SERVER_ADDR', ip)
        monkeypatch.setenv('SERVER_PORT', str(port))

        with open('./tests/fixtures/payment/create-no-method-auth.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.amount = amount

        with pytest.raises(
            InvalidCurrencyError,
            match='You must provide a currency before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.currency = currency

        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        # WARNING conditional in test body different in API V1 an V2
        if self.conf.version == Version.API_V1:
            assert isinstance(body.get('auth'), dict)
            assert 'return_url' not in body.get('auth')
            assert 'status' in body.get('auth')
            assert body.get('auth').get('status') == AuthStatus.REQUEST
        else:
            assert 'auth' in body
            assert body.get('auth') is True
            assert isinstance(obj.auth, AbstractObject)
            assert hasattr(obj.auth, 'return_url')
            assert obj.auth.return_url is None
            assert hasattr(obj.auth, 'status')
            assert obj.auth.status == AuthStatus.REQUESTED  # from fixtures

        assert 'card' not in body
        assert 'sepa' not in body
        assert 'device' not in body

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.card is None
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.live_mode is False
        assert obj.method is None
        assert obj.order_id is None
        assert obj.sepa is None

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_send_with_card(self, version):
        api_is_v1 = version == Version.API_V1
        self.conf.version = version
        obj = Payment()
        card = Card()

        customer = Customer()
        customer.name = self.random_string(15)
        customer.email = f'{self.random_string(15)}@example.org'
        customer.mobile = self.random_mobile()

        with open('./tests/fixtures/payment/create-card.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        # WARNING conditional in test
        if not api_is_v1:
            # For V2 we add a card and a customer Response, because we send them before the payment
            with open('./tests/fixtures/customer/create-customer.json') as opened_file:
                content = opened_file.read()
            responses.add(responses.POST, customer.uri, body=content)

            with open('./tests/fixtures/card/create-card.json') as opened_file:
                content = opened_file.read()
            responses.add(responses.POST, card.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.amount = self.random_integer(50, 999999)

        with pytest.raises(
            InvalidCurrencyError,
            match='You must provide a currency before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.currency = 'eur'
        obj.card = card
        obj.customer = customer

        with pytest.raises(
            MissingPaymentMethodError,
            match='Your card is incomplete.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        card.cvc = self.random_string(3)
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.number = '4111111111111111'

        assert obj.send() == obj
        # As we send customer and sepa beforehand, we have 3 API calls instead of 1 in API V1
        # the data we obtain are unchanged
        # WARNING conditional in test
        assert len(responses.calls) == 1 if api_is_v1 else 3

        # Data from fixture
        assert obj.id == 'paym_KIVaaHi7G8QAYMQpQOYBrUQE'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1538564253
        assert obj.created == obj.created_at
        assert obj.amount == 100
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.customer == customer
        assert obj.description == 'le test restfull v1'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert customer.id == 'cust_9Cle7TXKkjhwqcWx4Kl5cQYk'

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_send_with_sepa(self, version):
        api_is_v1 = version == Version.API_V1
        self.conf.version = version
        payment = Payment()
        sepa = Sepa()

        customer = Customer()
        customer.name = self.random_string(15)
        customer.email = f'{self.random_string(15)}@example.org'
        customer.mobile = self.random_mobile()

        with open('./tests/fixtures/payment/create-sepa.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, payment.uri, body=content)

        # WARNING conditional in test
        if not api_is_v1:
            # For V2 we add a sepa and a customer Response, because we send them before the payment
            with open('./tests/fixtures/sepa/create-sepa.json') as opened_file:
                content = opened_file.read()
            responses.add(responses.POST, sepa.uri, body=content)
            with open('./tests/fixtures/customer/create-customer.json') as opened_file:
                content = opened_file.read()
            responses.add(responses.POST, customer.uri, body=content)
            with pytest.raises(
                InvalidAmountError,
                match='You must provide an amount before sending a payment.',
            ):
                payment.send()

        assert len(responses.calls) == 0

        payment.amount = self.random_integer(50, 999999)

        with pytest.raises(
            InvalidCurrencyError,
            match='You must provide a currency before sending a payment.',
        ):
            payment.send()

        assert len(responses.calls) == 0

        payment.currency = 'eur'
        payment.sepa = sepa
        payment.customer = customer

        with pytest.raises(
            MissingPaymentMethodError,
            match='Your SEPA account is incomplete.',
        ):
            payment.send()

        assert len(responses.calls) == 0

        sepa.bic = 'DEUTDEFF'  # Thx Wikipedia
        sepa.iban = 'DE91 1000 0000 0123 4567 89'  # Thx Wikipedia

        assert payment.send() == payment
        # As we send customer and sepa beforehand, we have 3 API calls instead of 1 in API V1
        # the data we obtain are unchanged
        # WARNING conditional in test
        assert len(responses.calls) == 1 if api_is_v1 else 3

        # Data from fixture
        assert payment.id == 'paym_5IptC9R1Wu2wKBR5cjM2so7k'
        assert isinstance(payment.created, date)
        assert payment.created.timestamp() == 1538564504
        assert payment.amount == 100
        assert payment.card is None
        assert payment.capture is True
        assert payment.currency == 'eur'
        assert payment.customer == customer
        assert payment.description == 'le test restfull v1'
        assert payment.live_mode is False
        assert payment.method == 'sepa'
        assert payment.order_id is None

        assert sepa.id == 'sepa_oazGliEo6BuqUlyCzE42hcNp'
        assert sepa.bic == 'ILADFRPP'
        # Iban is unchanged in send process
        assert sepa.iban == 'DE91100000000123456789'
        assert sepa.last4 == '2606'
        assert sepa.name == 'David Coaster'

        assert customer.id == 'cust_9Cle7TXKkjhwqcWx4Kl5cQYk'

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_sepa(self, version):
        self.conf.version = version
        obj = Payment()
        sepa = Sepa()

        assert obj.sepa is None
        assert obj.method is None

        obj.sepa = sepa

        assert obj.sepa == sepa
        assert obj.method == 'sepa'

        with pytest.raises(
            InvalidSepaError,
            match='You must provide a valid instance of Sepa.',
        ):
            obj.sepa = self.random_integer(2)

        with pytest.raises(
            InvalidSepaError,
            match='You must provide a valid instance of Sepa.',
        ):
            obj.sepa = self.random_string(2)

        obj = Payment(self.random_string(29))

        params = {
            'sepa': {
                'id': self.random_string(29),
            },
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.sepa, Sepa)
        assert obj.sepa.id == params['sepa']['id']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_status(self, version):
        self.conf.version = version
        obj = Payment()
        status = self.random_string(10)

        assert obj.status is None

        obj.status = status

        assert obj.status == status
        assert obj.to_json().find(f'"status":"{status}"') > 0

        with pytest.raises(
            InvalidStatusError,
            match='Status must be a string.',
        ):
            obj.status = self.random_integer(20)

        obj = Payment(self.random_string(29))
        params = {
            'status': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.status == params['status']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('version', TestHelper.version_provider())
    @responses.activate
    def test_unique_id(self, version):
        self.conf.version = version
        obj = Payment()
        unique_id = self.random_string(36)

        assert obj.unique_id is None

        obj.unique_id = unique_id

        assert obj.unique_id == unique_id

        with pytest.raises(
            InvalidPaymentUniqueIdError,
            match='Unique ID must be a string.',
        ):
            obj.unique_id = self.random_integer(20)

        with pytest.raises(
            InvalidPaymentUniqueIdError,
            match='Unique ID must be 36 characters maximum.',
        ):
            obj.unique_id = self.random_string(40)

        obj = Payment(self.random_string(29))
        params = {
            'unique_id': self.random_string(36),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.unique_id == params['unique_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

        # Works with uuid

        obj = Payment()
        unique_id = uuid.uuid4()

        assert obj.unique_id is None

        obj.unique_id = unique_id

        assert obj.unique_id == str(unique_id)

    # endregion

    # region V1
    # The auth is sent as a bool in V2 but as an object in V1
    # This is a big change so we need two separate test
    def test_auth_v1(self, version=Version.API_V1):
        payment = Payment()
        auth = Auth()
        self.conf.version = version
        assert payment.auth is None
        payment.auth = auth
        assert payment.auth == auth

        with pytest.raises(
            InvalidAuthError,
            match='You must provide a valid instance of Auth',
        ):
            payment.auth = self.random_integer(2)

        with pytest.raises(InvalidUrlError):
            payment.auth = self.random_string(2)

        return_url = 'https://www.example.org/?' + self.random_string(15)
        payment.auth = return_url

        assert isinstance(payment.auth, Auth)
        assert payment.auth.return_url == return_url
        assert payment.auth.status == AuthStatus.REQUEST

        payment.auth = True

        assert isinstance(payment.auth, Auth)
        assert payment.auth.return_url is None
        assert payment.auth.status == AuthStatus.REQUEST

        payment.auth = False

        assert isinstance(payment.auth, Auth)
        assert payment.auth.return_url is None
        assert payment.auth.status == AuthStatus.REQUEST

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auth_and_device_object_v1(self, version=Version.API_V1):
        obj = Payment()
        card = Card()
        auth = Auth()
        device = Device()
        self.conf.version = version

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = f'https://www.example.org/?f{self.random_string(50)}'

        obj.amount = amount
        obj.auth = auth
        obj.currency = currency
        obj.card = card
        obj.device = device

        auth.return_url = return_url

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        device.ip = ip

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0

        device.port = port
        # The payment should always be the full object not only in V1 the true check is only for sending the object.
        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert isinstance(body.get('auth'), dict)
        assert 'return_url' in body.get('auth')
        assert body.get('auth').get('return_url') == return_url
        assert 'status' in body.get('auth')
        assert body.get('auth').get('status') == AuthStatus.REQUEST

        assert 'card' in body
        assert isinstance(body.get('card'), dict)
        assert 'cvc' in body.get('card')
        assert body.get('card').get('cvc') == cvc
        assert 'exp_month' in body.get('card')
        assert body.get('card').get('exp_month') == exp_month
        assert 'exp_year' in body.get('card')
        assert body.get('card').get('exp_year') == exp_year
        assert 'number' in body.get('card')
        assert body.get('card').get('number') == number

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.auth == auth
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auth_return_url_v1(self, monkeypatch, version=Version.API_V1):
        self.conf.version = version
        obj = Payment()
        card = Card()

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = 'https://www.example.org/?' + self.random_string(50)

        obj.amount = amount
        obj.auth = return_url
        obj.currency = currency
        obj.card = card

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_ADDR', ip)

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_PORT', str(port))

        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert isinstance(body.get('auth'), dict)
        assert 'return_url' in body.get('auth')
        assert body.get('auth').get('return_url') == return_url
        assert 'status' in body.get('auth')
        assert body.get('auth').get('status') == AuthStatus.REQUEST

        assert 'card' in body
        assert isinstance(body.get('card'), dict)
        assert 'cvc' in body.get('card')
        assert body.get('card').get('cvc') == cvc
        assert 'exp_month' in body.get('card')
        assert body.get('card').get('exp_month') == exp_month
        assert 'exp_year' in body.get('card')
        assert body.get('card').get('exp_year') == exp_year
        assert 'number' in body.get('card')
        assert body.get('card').get('number') == number

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auth_object_v1(self, monkeypatch, version=Version.API_V1):
        self.conf.version = version
        obj = Payment()
        card = Card()
        auth = Auth()

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = f'https://www.example.org/?{self.random_string(50)}'

        obj.amount = amount
        obj.auth = auth
        obj.currency = currency
        obj.card = card

        auth.return_url = return_url

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_ADDR', ip)

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0
        monkeypatch.setenv('SERVER_PORT', str(port))
        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)
        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert isinstance(body.get('auth'), dict)
        assert 'return_url' in body.get('auth')
        assert body.get('auth').get('return_url') == return_url
        assert 'status' in body.get('auth')
        assert body.get('auth').get('status') == AuthStatus.REQUEST

        assert 'card' in body
        assert isinstance(body.get('card'), dict)
        assert 'cvc' in body.get('card')
        assert body.get('card').get('cvc') == cvc
        assert 'exp_month' in body.get('card')
        assert body.get('card').get('exp_month') == exp_month
        assert 'exp_year' in body.get('card')
        assert body.get('card').get('exp_year') == exp_year
        assert 'number' in body.get('card')
        assert body.get('card').get('number') == number

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.auth == auth
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auto_create_device_v1(self, monkeypatch, version=Version.API_V1):
        self.conf.version = version
        obj = Payment()
        card = Card()

        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        port = self.random_integer(1, 65535)

        monkeypatch.setenv('SERVER_ADDR', ip)
        monkeypatch.setenv('SERVER_PORT', str(port))

        with open('./tests/fixtures/payment/create-card.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'

        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        number = '4111111111111111'

        obj.amount = amount
        obj.currency = currency
        obj.card = card

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        assert obj.send()
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'card' in body
        assert isinstance(body.get('card'), dict)
        assert 'cvc' in body.get('card')
        assert body.get('card').get('cvc') == cvc
        assert 'exp_month' in body.get('card')
        assert body.get('card').get('exp_month') == exp_month
        assert 'exp_year' in body.get('card')
        assert body.get('card').get('exp_year') == exp_year
        assert 'number' in body.get('card')
        assert body.get('card').get('number') == number

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_KIVaaHi7G8QAYMQpQOYBrUQE'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1538564253
        assert obj.amount == 100
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'le test restfull v1'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None
        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.device, Device)
        assert obj.device.ip == ip
        assert obj.device.port == port

    # We check that the payment.card sent is the same as the payment.card received in V1
    # we also make many check on calls, if we made one test it would have been less readable
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_delayed_capture_v1(self, version=Version.API_V1):
        self.conf.version = version
        obj = Payment()

        # Prepare responses
        with open(
            './tests/fixtures/payment/create-card-status-null-no-method.json'
        ) as opened:
            fixture = opened.read()
        responses.add(responses.POST, obj.uri, body=fixture)
        payment_id = json.loads(fixture)['id']
        uri = f'{obj.uri}{payment_id}'

        with open(
            './tests/fixtures/payment/create-card-status-null-with-card.json'
        ) as opened:
            responses.add(responses.PATCH, uri, body=opened.read())

        with open(
            './tests/fixtures/payment/create-card-status-to-capture.json'
        ) as opened:
            responses.add(responses.PATCH, uri, body=opened.read())

        obj.amount = self.random_integer(50, 999999)
        obj.currency = 'eur'

        # Payment creation

        assert obj.send() == obj
        assert len(responses.calls) == 1

        assert obj.card is None
        assert obj.status is None

        # Add card

        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        number = '4242424242424242'

        obj.card = Card()
        obj.card.cvc = cvc
        obj.card.exp_month = exp_month
        obj.card.exp_year = exp_year
        obj.card.number = number

        assert obj.send() == obj
        assert len(responses.calls) == 2

        body = json.loads(responses.calls[1].request.body)

        assert len(body.keys()) == 1

        assert 'card' in body
        assert isinstance(body.get('card'), dict)
        assert 'cvc' in body.get('card')
        assert body.get('card').get('cvc') == cvc
        assert 'exp_month' in body.get('card')
        assert body.get('card').get('exp_month') == exp_month
        assert 'exp_year' in body.get('card')
        assert body.get('card').get('exp_year') == exp_year
        assert 'number' in body.get('card')
        assert body.get('card').get('number') == number

        # Change status

        obj.status = PaymentStatus.CAPTURE

        assert obj.send() == obj
        assert len(responses.calls) == 3

        body = json.loads(responses.calls[2].request.body)

        assert len(body.keys()) == 1

        assert 'status' in body
        assert body.get('status') == PaymentStatus.CAPTURE

    # We check that the payment.customer sent is the same as the payment.customer received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_without_method_v1(self, version=Version.API_V1):
        self.conf.version = version
        obj = Payment()

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        email = f'{self.random_string(15)}@example.org'
        mobile = self.random_mobile()
        name = self.random_string(15)

        customer = Customer()
        customer.name = name
        customer.email = email
        customer.mobile = mobile

        obj.customer = customer

        with open('./tests/fixtures/payment/create-no-method.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.amount = amount

        with pytest.raises(
            InvalidCurrencyError,
            match='You must provide a currency before sending a payment.',
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.currency = currency

        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data sent
        body = json.loads(responses.calls[0].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'card' not in body
        assert 'sepa' not in body

        assert 'customer' in body
        assert isinstance(body.get('customer'), dict)
        assert 'email' in body.get('customer')
        assert body.get('customer').get('email') == email
        assert 'mobile' in body.get('customer')
        assert body.get('customer').get('mobile') == mobile
        assert 'name' in body.get('customer')
        assert body.get('customer').get('name') == name

        # Data from fixture
        assert obj.id == 'paym_pia9ossoqujuFFbX0HdS3FLi'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1562085759
        assert obj.amount == 10000
        assert obj.card is None
        assert obj.currency == 'eur'
        assert obj.customer == customer
        assert obj.description == 'Test payment without any card or sepa account'
        assert obj.live_mode is False
        assert obj.method is None
        assert obj.order_id is None
        assert obj.sepa is None

        assert customer.id == 'cust_IYsHodYTugeBndSIOdm6rnBA'

    # The endpoint is not the same in V1 and V2 this is a big change so we separate the two test
    @pytest.mark.parametrize('host', TestHelper.host_provider())
    @responses.activate
    def test_uri_v1(self, host, version=Version.API_V1):
        self.conf.version = version
        self.conf.host = host
        obj = Payment()
        uid = self.random_string(29)
        assert obj.uri == f'https://{self.conf.host}/v{self.conf.version}/checkout/'

        obj.hydrate(id=uid)

        assert (
            obj.uri == f'https://{self.conf.host}/v{self.conf.version}/checkout/{uid}'
        )

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)

    # endregion

    # region V2
    # The auth is sent as a bool in V2 but as an object in V1
    # This is a big change so we need two separate test
    def test_auth_v2(self, version=Version.API_V2):
        payment = Payment()
        auth = Auth()
        self.conf.version = version

        assert payment.auth is None

        payment.auth = auth

        assert payment.auth.to_json() == 'true'
        assert payment.auth.to_json_repr()

        # Now everything except false send an auth
        with pytest.raises(
            InvalidAuthError,
            match='You must provide a valid instance of Auth',
        ):
            payment.auth = self.random_integer(2)

        with pytest.raises(InvalidUrlError):
            payment.auth = self.random_string(2)

        payment = Payment()
        return_url = 'https://www.example.org/?' + self.random_string(15)
        payment.auth = return_url

        assert isinstance(payment.auth, Auth)
        assert payment.auth.to_json_repr() is True
        assert payment.auth.return_url == return_url
        assert payment.auth.status == AuthStatus.REQUEST
        payment = Payment()
        payment.auth = True

        assert isinstance(payment.auth, Auth)
        assert payment.auth.to_json_repr() is True
        assert payment.auth.return_url is None
        assert payment.auth.status == AuthStatus.REQUEST
        assert payment.auth.to_json() == 'true'

        payment.auth = False

        assert isinstance(payment.auth, Auth)
        assert payment.auth.to_json_repr() is True
        assert payment.auth.return_url is None
        assert payment.auth.status == AuthStatus.REQUEST
        assert payment.auth.to_json() == 'true'

    @responses.activate
    def test_send_auth_and_device_object_v2(self, version=Version.API_V2):
        obj = Payment()
        card = Card()
        auth = Auth()
        device = Device()
        self.conf.version = version

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with open('./tests/fixtures/card/create-card.json') as opened:
            content = opened.read()

        responses.add(responses.POST, card.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = 'https://www.free.fr'  # from fixtures

        obj.amount = amount
        obj.auth = auth
        obj.currency = currency
        obj.card = card
        obj.device = device

        auth.return_url = return_url

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        device.ip = ip

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0

        device.port = port
        # The payment should always be the full object not only in V1 the true check is only for sending the object.
        assert obj.send() == obj
        assert len(responses.calls) == 2

        card_body = json.loads(responses.calls[0].request.body)
        assert isinstance(card_body, dict)
        assert 'cvc' in card_body
        assert card_body.get('cvc') == cvc
        assert 'exp_month' in card_body
        assert card_body.get('exp_month') == exp_month
        assert 'exp_year' in card_body
        assert card_body.get('exp_year') == exp_year
        assert 'number' in card_body
        assert card_body.get('number') == number
        # Data sent
        body = json.loads(responses.calls[1].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert body.get('auth') is True
        assert isinstance(obj.auth, AbstractObject)
        assert hasattr(obj.auth, 'return_url')
        assert obj.auth.return_url == return_url
        assert hasattr(obj.auth, 'status')
        assert obj.auth.status == AuthStatus.AVAILABLE  # from fixtures

        assert 'card' in body
        assert isinstance(body.get('card'), str)

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.auth == auth
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auth_return_url_v2(self, monkeypatch, version=Version.API_V2):
        self.conf.version = version
        obj = Payment()
        card = Card()

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with open('./tests/fixtures/card/create-card.json') as opened:
            content = opened.read()

            # Save response
        responses.add(responses.POST, card.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = 'https://www.free.fr'  # from fixtures

        obj.amount = amount
        obj.auth = return_url
        obj.currency = currency
        obj.card = card

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_ADDR', ip)

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_PORT', str(port))

        assert obj.send() == obj
        assert len(responses.calls) == 2

        # Data sent
        card_body = json.loads(responses.calls[0].request.body)
        assert isinstance(card_body, dict)
        assert 'cvc' in card_body
        assert card_body.get('cvc') == cvc
        assert 'exp_month' in card_body
        assert card_body.get('exp_month') == exp_month
        assert 'exp_year' in card_body
        assert card_body.get('exp_year') == exp_year
        assert 'number' in card_body
        assert card_body.get('number') == number

        body = json.loads(responses.calls[1].request.body)
        assert 'card' in body
        assert isinstance(body.get('card'), str)
        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert body.get('auth') is True
        assert isinstance(obj.auth, AbstractObject)
        assert hasattr(obj.auth, 'return_url')
        assert obj.auth.return_url == return_url
        assert hasattr(obj.auth, 'status')
        assert obj.auth.status == AuthStatus.AVAILABLE  # from fixtures

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auth_object_v2(self, monkeypatch, version=Version.API_V2):
        self.conf.version = version
        obj = Payment()
        card = Card()
        auth = Auth()

        with open('./tests/fixtures/payment/create-card-auth.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with open('./tests/fixtures/card/create-card.json') as opened:
            content = opened.read()

        # Save response
        responses.add(responses.POST, card.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        number = '4111111111111111'
        port = self.random_integer(1, 65535)
        return_url = 'https://www.free.fr'  # from fixtures

        obj.amount = amount
        obj.auth = auth
        obj.currency = currency
        obj.card = card

        auth.return_url = return_url

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        with pytest.raises(InvalidIpAddressError):
            obj.send()

        assert len(responses.calls) == 0

        monkeypatch.setenv('SERVER_ADDR', ip)

        with pytest.raises(InvalidPortError):
            obj.send()

        assert len(responses.calls) == 0
        monkeypatch.setenv('SERVER_PORT', str(port))
        assert obj.send() == obj
        assert len(responses.calls) == 2

        # Data sent
        card_body = json.loads(responses.calls[0].request.body)
        assert isinstance(card_body, dict)
        assert 'cvc' in card_body
        assert card_body.get('cvc') == cvc
        assert 'exp_month' in card_body
        assert card_body.get('exp_month') == exp_month
        assert 'exp_year' in card_body
        assert card_body.get('exp_year') == exp_year
        assert 'number' in card_body
        assert card_body.get('number') == number

        body = json.loads(responses.calls[1].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'auth' in body
        assert body.get('auth') is True
        assert isinstance(obj.auth, AbstractObject)
        assert hasattr(obj.auth, 'return_url')
        assert obj.auth.return_url == return_url
        assert hasattr(obj.auth, 'status')
        assert obj.auth.status == AuthStatus.AVAILABLE  # From fixtures

        assert 'card' in body
        assert isinstance(body.get('card'), str)

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_RMLytyx2xLkdXkATKSxHOlvC'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1567094428
        assert obj.amount == 1337
        assert obj.auth == auth
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'Auth test'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None

        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.auth, Auth)
        assert obj.auth.return_url == 'https://www.free.fr'
        assert obj.auth.status == AuthStatus.AVAILABLE

        assert isinstance(obj.device, Device)
        assert obj.device.http_accept == 'text/html'
        assert obj.device.ip == '212.27.48.10'
        assert obj.device.languages is None
        assert obj.device.port == 1337
        assert obj.device.user_agent is None

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_auto_create_device_v2(self, monkeypatch, version=Version.API_V2):
        self.conf.version = version
        obj = Payment()
        card = Card()

        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        port = self.random_integer(1, 65535)

        monkeypatch.setenv('SERVER_ADDR', ip)
        monkeypatch.setenv('SERVER_PORT', str(port))

        with open('./tests/fixtures/payment/create-card.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        amount = self.random_integer(50, 999999)
        currency = 'eur'

        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        number = '4111111111111111'

        obj.amount = amount
        obj.currency = currency
        obj.card = card

        card.cvc = cvc
        card.exp_month = exp_month
        card.exp_year = exp_year
        card.number = number

        # We create the card call
        with open('./tests/fixtures/card/create-card.json') as opened_file:
            content = opened_file.read()

        responses.add(responses.POST, card.uri, body=content)

        assert obj.send()
        assert len(responses.calls) == 2

        # Data sent
        card_body = json.loads(responses.calls[0].request.body)
        assert isinstance(card_body, dict)
        assert 'cvc' in card_body
        assert card_body.get('cvc') == cvc
        assert 'exp_month' in card_body
        assert card_body.get('exp_month') == exp_month
        assert 'exp_year' in card_body
        assert card_body.get('exp_year') == exp_year
        assert 'number' in card_body
        assert card_body.get('number') == number

        body = json.loads(responses.calls[1].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'card' in body

        assert 'device' in body
        assert isinstance(body.get('device'), dict)
        assert 'ip' in body.get('device')
        assert body.get('device').get('ip') == ip
        assert 'port' in body.get('device')
        assert body.get('device').get('port') == port

        # Data from fixture
        assert obj.id == 'paym_KIVaaHi7G8QAYMQpQOYBrUQE'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1538564253
        assert obj.amount == 100
        assert obj.capture is True
        assert obj.card == card
        assert obj.currency == 'eur'
        assert obj.description == 'le test restfull v1'
        assert obj.method == 'card'
        assert obj.order_id is None
        assert obj.sepa is None
        assert card.id == 'card_xognFbZs935LMKJYeHyCAYUd'
        assert card.brand == 'mastercard'
        assert card.country == 'US'
        assert card.exp_month == 2
        assert card.exp_year == 2020
        assert card.last4 == '4444'
        assert card.name is None
        # Number is unchanged in send process
        assert card.number == '4111111111111111'
        assert card.zip_code is None

        assert isinstance(obj.device, Device)
        assert obj.device.ip == ip
        assert obj.device.port == port

    # We check that the payment.card sent is the same as the payment.card received in V1
    # This is not how the API v2 work so we need two separate test
    # we also make many check on calls, if we made one test it would have been less readable
    @responses.activate
    def test_send_delayed_capture_v2(self, version=Version.API_V2):
        self.conf.version = version
        obj = Payment()

        # Prepare responses
        with open(
            './tests/fixtures/payment/create-card-status-null-no-method.json'
        ) as opened:
            fixture = opened.read()
        responses.add(responses.POST, obj.uri, body=fixture)
        payment_id = json.loads(fixture)['id']
        uri = f'{obj.uri}{payment_id}'

        with open(
            './tests/fixtures/payment/create-card-status-null-with-card.json'
        ) as opened:
            responses.add(responses.PATCH, uri, body=opened.read())

        with open(
            './tests/fixtures/payment/create-card-status-to-capture.json'
        ) as opened:
            responses.add(responses.PATCH, uri, body=opened.read())

        obj.amount = self.random_integer(50, 999999)
        obj.currency = 'eur'

        # Payment creation

        assert obj.send() == obj
        assert len(responses.calls) == 1

        assert obj.card is None
        assert obj.status is None

        # Add card

        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        number = '4242424242424242'

        obj.card = Card()
        obj.card.cvc = cvc
        obj.card.exp_month = exp_month
        obj.card.exp_year = exp_year
        obj.card.number = number
        # We create the card object directly in our payment we want to be sure this will still send the card correctly
        with open('./tests/fixtures/card/create-card.json') as opened:
            responses.add(responses.POST, obj.card.uri, body=opened.read())

        assert obj.send() == obj
        assert len(responses.calls) == 3

        card_body = json.loads(responses.calls[1].request.body)
        assert isinstance(card_body, dict)
        assert 'cvc' in card_body
        assert card_body.get('cvc') == cvc
        assert 'exp_month' in card_body
        assert card_body.get('exp_month') == exp_month
        assert 'exp_year' in card_body
        assert card_body.get('exp_year') == exp_year
        assert 'number' in card_body
        assert card_body.get('number') == number

        body = json.loads(responses.calls[2].request.body)

        assert len(body.keys()) == 1

        assert 'card' in body
        assert isinstance(body.get('card'), str)

        # Change status

        obj.status = PaymentStatus.CAPTURE

        assert obj.send() == obj
        assert len(responses.calls) == 4

        body = json.loads(responses.calls[3].request.body)

        assert len(body.keys()) == 1

        assert 'status' in body
        assert body.get('status') == PaymentStatus.CAPTURE

    # We check that the payment.customer sent is the same as the payment.customer received in V1
    # This is not how the API v2 work so we need two separate test
    @responses.activate
    def test_send_without_method_v2(self, version=Version.API_V2):
        self.conf.version = version
        obj = Payment()

        amount = self.random_integer(50, 999999)
        currency = 'eur'
        email = self.random_string(15) + '@example.org'
        mobile = self.random_mobile()
        name = self.random_string(15)

        customer = Customer()
        customer.name = name
        customer.email = email
        customer.mobile = mobile

        obj.customer = customer

        with open('./tests/fixtures/payment/create-no-method.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

        with open('./tests/fixtures/customer/create-customer.json') as opened_file:
            content = opened_file.read()
        responses.add(responses.POST, customer.uri, body=content)

        with pytest.raises(
            InvalidAmountError,
            match='You must provide an amount before sending a payment.',
        ):
            obj.send()

        assert not responses.calls

        obj.amount = amount

        with pytest.raises(
            InvalidCurrencyError,
            match='You must provide a currency before sending a payment.',
        ):
            obj.send()

        assert not responses.calls

        obj.currency = currency

        assert obj.send() == obj
        assert len(responses.calls) == 2

        # Data sent
        print(responses.calls[0].request.body)
        customer_body = json.loads(responses.calls[0].request.body)

        assert isinstance(customer_body, dict)
        assert 'email' in customer_body
        assert customer_body.get('email') == email
        assert 'mobile' in customer_body
        assert customer_body.get('mobile') == mobile
        assert 'name' in customer_body
        assert customer_body.get('name') == name

        body = json.loads(responses.calls[1].request.body)

        assert 'amount' in body
        assert body.get('amount') == amount
        assert 'currency' in body
        assert body.get('currency') == currency

        assert 'card' not in body
        assert 'sepa' not in body

        assert 'customer' in body
        assert isinstance(body.get('customer'), str)

        # Data from fixture
        assert obj.id == 'paym_pia9ossoqujuFFbX0HdS3FLi'
        assert isinstance(obj.created, date)
        assert obj.created.timestamp() == 1562085759
        assert obj.amount == 10000
        assert obj.card is None
        assert obj.currency == 'eur'
        assert obj.customer == customer
        assert obj.description == 'Test payment without any card or sepa account'
        assert obj.live_mode is False
        assert obj.method is None
        assert obj.order_id is None
        assert obj.sepa is None

        assert customer.id == 'cust_IYsHodYTugeBndSIOdm6rnBA'

    # The endpoint is not the same in V1 and V2 this is a big change so we separate the two test
    @pytest.mark.parametrize('host', TestHelper.host_provider())
    @responses.activate
    def test_uri_v2(self, host, version=Version.API_V2):
        self.conf.version = version
        self.conf.host = host
        obj = Payment()
        uid = self.random_string(29)
        assert obj.uri == f'https://{self.conf.host}/v{self.conf.version}/payments/'

        obj.hydrate(id=uid)

        assert (
            obj.uri == f'https://{self.conf.host}/v{self.conf.version}/payments/{uid}'
        )

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)


# endregion
