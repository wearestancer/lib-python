"""Functional tests for payment object"""

import platform
import pytest

from iliad_payment import Auth
from iliad_payment import AuthStatus
from iliad_payment import Card
from iliad_payment import Config
from iliad_payment import Customer
from iliad_payment import Device
from iliad_payment import Payment
from iliad_payment.exceptions import NotFoundError
from .TestHelper import TestHelper


class TestFunctionalPayment(TestHelper):
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
    def test_send(self, currency):
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
        assert obj.send() == obj
        assert obj.id is not None

        uid = obj.id
        card_uid = card.id
        customer_uid = customer.id

        # If sent, we can get it
        obj = Payment(uid)

        assert obj.amount == amount
        assert obj.currency == currency
        assert obj.description == desc

        assert obj.card.id == card_uid
        assert obj.customer.id == customer_uid

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_send_with_authentification(self, currency):
        amount = self.random_integer(50, 99999)
        description = 'Automatic auth test for Python, {:.2f} {}'.format(amount / 100, currency)
        return_url = 'https://www.example.org/?' + self.random_string(30)

        ip = self.ip_provider(True)
        port = self.random_integer(1, 65534)

        device = Device(ip=ip, port=port)

        card = Card()
        card.cvc = str(self.random_integer(100, 999))
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.number = self.get_card_number()

        payment = Payment()
        payment.amount = amount
        payment.auth = return_url
        payment.card = card
        payment.currency = currency
        payment.description = description
        payment.device = device

        assert payment.send() == payment
        assert payment.id is not None
        assert payment.id.startswith('paym_')
        assert payment.status is None

        assert isinstance(payment.auth, Auth)
        assert payment.auth.return_url == return_url
        assert payment.auth.status == AuthStatus.AVAILABLE
        assert payment.auth.redirect_url is not None
        assert payment.auth.redirect_url.startswith('https://3ds.')

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_send_for_payment_page(self, currency):
        amount = self.random_integer(50, 99999)
        description = 'Payment page test for Python, {:.2f} {}'.format(amount / 100, currency)
        return_url = 'https://www.example.org/?' + self.random_string(30)

        payment = Payment()
        payment.amount = amount
        payment.currency = currency
        payment.description = description
        payment.return_url = return_url

        assert payment.send() == payment
        assert payment.id is not None
        assert payment.id.startswith('paym_')
        assert payment.method is None
        assert payment.status is None

        assert isinstance(payment.auth, Auth)
        assert payment.auth.status == AuthStatus.REQUESTED
        assert payment.auth.return_url is None
        assert payment.auth.redirect_url is None

        config = Config()

        keys = config.keys
        fake_public_key = 'p' + config.secret_key[1:]
        config.keys = fake_public_key

        assert payment.payment_page_url is not None
        assert payment.payment_page_url.startswith('https://payment')
        assert payment.payment_page_url.find(fake_public_key) > 0
        assert payment.payment_page_url.find(payment.id) > 0

        config.keys = keys
