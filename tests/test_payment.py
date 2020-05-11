"""Test payment object"""

from datetime import date
import json
import pytest
import responses

from iliad_payment import Auth
from iliad_payment import Card
from iliad_payment import Customer
from iliad_payment import Device
from iliad_payment import Payment
from iliad_payment import Refund
from iliad_payment import Sepa
from iliad_payment.core import AbstractAmount
from iliad_payment.core import AbstractCountry
from iliad_payment.core import AbstractObject
from iliad_payment.exceptions import IliadNotImplementedError
from iliad_payment.exceptions import InvalidAmountError
from iliad_payment.exceptions import InvalidAuthError
from iliad_payment.exceptions import InvalidCardError
from iliad_payment.exceptions import InvalidCurrencyError
from iliad_payment.exceptions import InvalidCustomerError
from iliad_payment.exceptions import InvalidDeviceError
from iliad_payment.exceptions import InvalidPaymentCaptureError
from iliad_payment.exceptions import InvalidPaymentDescriptionError
from iliad_payment.exceptions import InvalidPaymentOrderIdError
from iliad_payment.exceptions import InvalidSepaError
from iliad_payment.exceptions import MissingPaymentMethodError
from iliad_payment.status import RefundStatus
from .TestHelper import TestHelper


class TestPayment(TestHelper):
    def test_class(self):
        assert issubclass(Payment, AbstractCountry)
        assert issubclass(Payment, AbstractAmount)
        assert issubclass(Payment, AbstractObject)

        attrs = Payment._get_allowed_attributes()

        assert isinstance(attrs, list)
        assert 'amount' in attrs
        assert 'capture' in attrs
        assert 'card' in attrs
        assert 'currency' in attrs
        assert 'customer' in attrs
        assert 'description' in attrs
        assert 'order_id' in attrs
        assert 'sepa' in attrs

    @responses.activate
    def test_amount(self):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag and auto population

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

    def test_auth(self):
        obj = Payment()
        auth = Auth()

        assert obj.auth is None

        obj.auth = auth

        assert obj.auth == auth

        with pytest.raises(
            InvalidAuthError,
            match='You must provide a valid instance of Auth',
        ):
            obj.auth = self.random_integer(2)

        with pytest.raises(
            InvalidAuthError,
            match='You must provide a valid instance of Auth',
        ):
            obj.auth = self.random_string(2)

    @responses.activate
    def test_capture(self):
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

    @responses.activate
    def test_card(self):
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

    @responses.activate
    def test_customer(self):
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

    @responses.activate
    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_currency(self, currency):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag and auto population

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

    @responses.activate
    def test_description(self):
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

    def test_delete(self):
        obj = Payment(self.random_string(29))

        with pytest.raises(
            IliadNotImplementedError,
            match=(
                'You are not allowed to delete a payment, '
                'you need to refund it instead.'
            ),
        ):
            obj.delete()

    def test_device(self):
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

    def test_hydrate(self):
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

    def test_is_success(self):
        obj = Payment()

        obj.hydrate(response_code='00')

        assert obj.is_success is True
        assert obj.is_error is False

        obj.hydrate(response_code=self.random_string(2))

        assert obj.is_success is False
        assert obj.is_error is True

    @responses.activate
    def test_live_mode(self):
        obj = Payment()

        assert obj.live_mode is None

        with pytest.raises(AttributeError):
            obj.live_mode = True

        obj = Payment(self.random_string(29))
        params = {
            'live_mode': True,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.live_mode is True
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_method(self):
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

    @responses.activate
    def test_order_id(self):
        obj = Payment()
        order_id = self.random_string(1, 24)

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
            match='Order id must be 24 characters maximum.',
        ):
            obj.order_id = self.random_string(25, 30)

        obj = Payment(self.random_string(29))
        params = {
            'order_id': self.random_string(1, 24),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.order_id == params['order_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_refund(self):
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
        refund2_content['id'] = 'refd_' + self.random_string(24)

        responses.reset()
        responses.add(responses.GET, obj.uri, json=payment_content)
        responses.add(responses.POST, ref.uri, json=refund1_content)
        responses.add(responses.POST, ref.uri, json=refund2_content)

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 0
        assert len(responses.calls) == 1

        assert obj.refund(refund1_amount) == obj
        assert len(responses.calls) == 2

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 1
        assert obj.refunds[0].id == refund1_content['id']
        assert obj.refunds[0].amount == refund1_amount

        with pytest.raises(InvalidAmountError) as err:
            obj.refund(paid)

        assert str(err.value) == (
            'You are trying to refund ({0:.2f} {2}) '
            'more than possible ({1:.2f} {2}).'
        ).format(paid / 100, refund2_amount / 100, obj.currency.upper())

        assert obj.refund() == obj
        assert len(responses.calls) == 3

        assert isinstance(obj.refunds, list)
        assert len(obj.refunds) == 2
        assert obj.refunds[0].id == refund1_content['id']
        assert obj.refunds[0].amount == refund1_amount
        assert obj.refunds[1].id == refund2_content['id']
        assert obj.refunds[1].amount == refund2_amount

        assert obj.is_not_modified

    @responses.activate
    def test_refundable_amount(self):
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

    @responses.activate
    def test_refunded_amount(self):
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

    @responses.activate
    def test_response_code(self):
        obj = Payment()

        assert obj.response_code is None

        with pytest.raises(AttributeError):
            obj.response_code = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'response_code': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.response_code == params['response_code']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_response_message(self):
        obj = Payment()

        assert obj.response_message is None

        with pytest.raises(AttributeError):
            obj.response_message = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'response_code': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.response_code == params['response_code']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_send_with_card(self):
        obj = Payment()

        card = Card()

        customer = Customer()
        customer.name = self.random_string(15)
        customer.email = self.random_string(15) + '@example.org'
        customer.mobile = self.random_mobile()

        with open('./tests/fixtures/payment/create-card.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

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

        with pytest.raises(
            MissingPaymentMethodError,
            match=(
                'You must provide a valid credit card '
                'or SEPA account before sending a payment.'
            ),
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.card = card
        obj.customer = customer

        with pytest.raises(
            MissingPaymentMethodError,
            match=(
                'You must provide a valid credit card '
                'or SEPA account before sending a payment. '
                'Your card is incomplete.'
            ),
        ):
            obj.send()

        assert len(responses.calls) == 0

        card.cvc = self.random_string(3)
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.number = '4111111111111111'

        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data from fixture
        assert obj.id == 'paym_KIVaaHi7G8QAYMQpQOYBrUQE'
        assert isinstance(obj.created, date)
        assert int(obj.created.strftime('%s')) == 1538564253
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

    @responses.activate
    def test_send_with_sepa(self):
        obj = Payment()

        sepa = Sepa()

        customer = Customer()
        customer.name = self.random_string(15)
        customer.email = self.random_string(15) + '@example.org'
        customer.mobile = self.random_mobile()

        with open('./tests/fixtures/payment/create-sepa.json') as opened_file:
            content = opened_file.read()

        # Save response
        responses.add(responses.POST, obj.uri, body=content)

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

        with pytest.raises(
            MissingPaymentMethodError,
            match=(
                'You must provide a valid credit card '
                'or SEPA account before sending a payment.'
            ),
        ):
            obj.send()

        assert len(responses.calls) == 0

        obj.sepa = sepa
        obj.customer = customer

        with pytest.raises(
            MissingPaymentMethodError,
            match=(
                'You must provide a valid credit card '
                'or SEPA account before sending a payment. '
                'Your SEPA account is incomplete.'
            ),
        ):
            obj.send()

        assert len(responses.calls) == 0

        sepa.bic = 'DEUTDEFF'  # Thx Wikipedia
        sepa.iban = 'DE91 1000 0000 0123 4567 89'  # Thx Wikipedia

        assert obj.send() == obj
        assert len(responses.calls) == 1

        # Data from fixture
        assert obj.id == 'paym_5IptC9R1Wu2wKBR5cjM2so7k'
        assert isinstance(obj.created, date)
        assert int(obj.created.strftime('%s')) == 1538564504
        assert obj.amount == 100
        assert obj.card is None
        assert obj.capture is True
        assert obj.currency == 'eur'
        assert obj.customer == customer
        assert obj.description == 'le test restfull v1'
        assert obj.live_mode is False
        assert obj.method == 'sepa'
        assert obj.order_id is None

        assert sepa.id == 'sepa_oazGliEo6BuqUlyCzE42hcNp'
        assert sepa.bic == 'ILADFRPP'
        # Iban is unchanged in send process
        assert sepa.iban == 'DE91100000000123456789'
        assert sepa.last4 == '2606'
        assert sepa.name == 'David Coaster'

        assert customer.id == 'cust_9Cle7TXKkjhwqcWx4Kl5cQYk'

    @responses.activate
    def test_sepa(self):
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

    @responses.activate
    def test_status(self):
        obj = Payment()

        assert obj.status is None

        with pytest.raises(AttributeError):
            obj.status = self.random_string(29)

        obj = Payment(self.random_string(29))
        params = {
            'status': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.status == params['status']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_uri(self):
        obj = Payment()
        uid = self.random_string(29)

        assert obj.uri == 'https://api.iliad78.net/v1/checkout'

        obj.hydrate(id=uid)

        assert obj.uri == 'https://api.iliad78.net/v1/checkout/' + uid

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
