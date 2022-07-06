"""Functional tests for payment object"""

import platform
import pytest
import uuid

from stancer import Auth
from stancer import AuthStatus
from stancer import Card
from stancer import Config
from stancer import Customer
from stancer import Device
from stancer import Payment
from stancer import PaymentStatus
from stancer.exceptions import ConflictError
from stancer.exceptions import NotFoundError
from .TestHelper import TestHelper


class TestFunctionalPayment(TestHelper):
    def test_get(self):
        # 404 with an unknown payment (with a random id)
        with pytest.raises(NotFoundError) as error:
            obj = Payment(self.random_string(29))
            obj.amount

        assert error.value.message == 'No such payment {}'.format(obj.id)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404
        assert error.value.type == 'invalid_request_error'

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

    def test_list(self):
        order_id = self.random_string(36)
        unique_id = self.random_string(36)

        amount1 = self.random_integer(50, 100_00)
        currency1 = TestHelper.currency_provider(True)

        payment1 = Payment()
        payment1.amount = amount1
        payment1.currency = currency1
        payment1.description = 'Automatic test for payments list, {} {}, 1/2'.format(amount1 / 100, currency1.upper())
        payment1.order_id = order_id
        payment1.unique_id = unique_id

        payment1.card = Card()
        payment1.card.number = self.get_card_number()
        payment1.card.exp_month = self.random_integer(1, 12)
        payment1.card.exp_year = self.random_year()
        payment1.card.cvc = str(self.random_integer(100, 999))

        payment1.send()

        amount2 = self.random_integer(50, 100_00)
        currency2 = TestHelper.currency_provider(True)

        payment2 = Payment()
        payment2.amount = amount2
        payment2.currency = currency2
        payment2.description = 'Automatic test for payments list, {} {}, 2/2'.format(amount2 / 100, currency2.upper())
        payment2.order_id = order_id

        payment2.card = Card()
        payment2.card.number = self.get_card_number()
        payment2.card.exp_month = self.random_integer(1, 12)
        payment2.card.exp_year = self.random_year()
        payment2.card.cvc = str(self.random_integer(100, 999))

        payment2.send()

        counter = 0

        for payment in Payment.list(order_id=order_id):
            assert isinstance(payment, Payment)
            assert payment.id in (payment1.id, payment2.id)
            assert payment.order_id == order_id

            if payment.id == payment1.id:
                assert payment.amount == amount1
                assert payment.currency == currency1
                assert payment.unique_id == unique_id
            else:
                assert payment.amount == amount2
                assert payment.currency == currency2
                assert payment.unique_id is None

            counter += 1

        assert counter == 2

        counter = 0

        for payment in Payment.list(unique_id=unique_id):
            assert isinstance(payment, Payment)
            assert payment.id == payment1.id
            assert payment.amount == amount1
            assert payment.currency == currency1
            assert payment.order_id == order_id
            assert payment.unique_id == unique_id

            counter += 1

        assert counter == 1

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
        payment.auth = True
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

        assert payment.payment_page_url() is not None
        assert payment.payment_page_url().startswith('https://payment')
        assert payment.payment_page_url().find(fake_public_key) > 0
        assert payment.payment_page_url().find(payment.id) > 0

        config.keys = keys

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_send_path_status(self, currency):
        amount = self.random_integer(50, 99999)
        description = 'Patch status test for Python, {:.2f} {}'.format(amount / 100, currency)

        payment = Payment()
        payment.amount = amount
        payment.currency = currency
        payment.description = description

        assert payment.send() == payment
        assert payment.id is not None
        assert payment.id.startswith('paym_')
        assert payment.method is None
        assert payment.status is None

        # We have a payment without status, we need to add a method

        card = Card(
            cvc=str(self.random_integer(100, 999)),
            exp_month=self.random_integer(1, 12),
            exp_year=self.random_year(),
            number=self.get_card_number(),
        )
        payment.card = card

        assert payment.send() == payment
        assert payment.method == 'card'
        assert payment.status is None

        assert card.id is not None
        assert card.id.startswith('card_')

        # Still no status, but we can modify it, first we will ask an authorization

        payment.status = PaymentStatus.AUTHORIZE

        assert payment.send() == payment
        assert payment.status == PaymentStatus.AUTHORIZED

        # Let's try a capture

        payment.status = PaymentStatus.CAPTURE

        assert payment.send() == payment
        assert payment.status == PaymentStatus.TO_CAPTURE

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_send_with_unique_id(self, currency):
        obj = Payment()

        amount = self.random_integer(50, 10000)
        desc = 'Python {} automatic test for `unique_id`, {:.2f} {}'.format(
            platform.python_version(),
            amount / 100,
            currency.upper(),
        )
        unique_id = uuid.uuid4()

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
        obj.unique_id = unique_id

        assert obj.id is None
        assert obj.send() == obj
        assert obj.id is not None
        assert obj.id.startswith('paym_')

        uid = obj.id
        card_uid = card.id
        customer_uid = customer.id

        # If sent, we can get it
        obj = Payment(uid)

        assert obj.amount == amount
        assert obj.currency == currency
        assert obj.description == desc
        assert obj.unique_id == str(unique_id)

        assert obj.card.id == card_uid
        assert obj.customer.id == customer_uid

        # But we can not create another payment with the same unique ID

        obj = Payment()

        obj.amount = self.random_integer(50, 9999)
        obj.card = card
        obj.currency = currency
        obj.unique_id = unique_id

        with pytest.raises(ConflictError):
            obj.send()
