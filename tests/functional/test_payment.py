"""Functional tests for payment object"""

import platform
import uuid

import pytest

from stancer.auth import Auth
from stancer.card import Card
from stancer.config import Config
from stancer.core.enum.version import Version
from stancer.customer import Customer
from stancer.device import Device
from stancer.exceptions import ConflictError
from stancer.exceptions import NotFoundError
from stancer.payment import Payment
from stancer.status.auth import AuthStatus
from stancer.status.payment import PaymentStatus

from .FunctionalTestHelper import FunctionalTestHelper


class TestFunctionalPayment(FunctionalTestHelper):
    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_get(self, version):
        self.conf.version = version
        # 404 with an unknown payment (with a random id)
        with pytest.raises(NotFoundError) as error:
            obj = Payment(f'paym_{self.random_string(24)}')
            obj.amount

        assert error.value.message == self.get_not_found_message(obj)
        assert error.value.reason == 'Not Found'
        assert error.value.status_code == 404

        # Recover a valid payment
        obj = Payment('paym_9i0jdIWD7yYi5BVPYjKFjt2G')

        assert obj.amount == 8973
        assert obj.currency == 'eur'
        assert (
            obj.description == 'Python 3.12.3 automatic test for `unique_id`, 89.73 EUR'
        )
        assert obj.method == 'card'

        assert isinstance(obj.card, Card)
        assert obj.card.id == 'card_QhPTMv7tHdkTIHEhTc8RVLVL'

        assert isinstance(obj.customer, Customer)
        assert obj.customer.id == 'cust_nqjcoW1NscmX6TP3QvkxU5pG'

    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_list(self, version):
        self.conf.version = version
        order_id = self.random_string(36)
        unique_id = self.random_string(36)

        amount1 = self.random_integer(50, 100_00)
        currency1 = FunctionalTestHelper.currency_provider(True)

        payment1 = Payment()
        payment1.amount = amount1
        payment1.currency = currency1
        payment1.description = f'Automatic test for payments list, {amount1 / 100} {currency1.upper()}, 1/2'
        payment1.order_id = order_id
        payment1.unique_id = unique_id

        payment1.card = Card()
        payment1.card.number = self.get_card_number()
        payment1.card.exp_month = self.random_integer(1, 12)
        payment1.card.exp_year = self.random_year()
        payment1.card.cvc = str(self.random_integer(100, 999))

        payment1.send()

        amount2 = self.random_integer(50, 100_00)
        currency2 = FunctionalTestHelper.currency_provider(True)

        payment2 = Payment()
        payment2.amount = amount2
        payment2.currency = currency2
        payment2.description = f'Automatic test for payments list, {amount2 / 100} {currency2.upper()}, 2/2'
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

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_send(self, currency, version):
        self.conf.version = version
        obj = Payment()

        amount = self.random_integer(50, 10000)
        desc = f'Python {platform.python_version()} automatic test, {amount / 100:.2f} {currency.upper()}'

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

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_send_with_authentification(self, currency, version):
        self.conf.version = version
        amount = self.random_integer(50, 99999)
        description = f'Automatic auth test for Python, {amount / 100:.2f} {currency}'
        return_url = f'https://www.example.org/?{self.random_string(30)}'

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

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_send_for_payment_page(self, currency, version):
        self.conf.version = version
        amount = self.random_integer(50, 99999)
        description = f'Payment page test for Python, {amount / 100:.2f} {currency}'
        return_url = f'https://www.example.org/?{self.random_string(30)}'

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
        fake_public_key = f'p{config.secret_key[1:]}'
        config.keys = fake_public_key

        assert payment.payment_page_url() is not None
        assert payment.payment_page_url().startswith('https://payment')
        assert fake_public_key in payment.payment_page_url()

        config.keys = keys

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    def test_send_path_status_v1(self, currency, version=Version.API_V1):
        self.conf.version = version
        amount = self.random_integer(50, 99999)
        description = f'Patch status test for Python, {amount / 100:.2f} {currency}'

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

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    def test_send_path_status_v2(self, currency, version=Version.API_V2):
        self.conf.version = version

        amount = self.random_integer(50, 99999)
        description = f'Patch status test for Python, {amount / 100:.2f} {currency}'

        payment = Payment()
        payment.amount = amount
        payment.currency = currency
        payment.description = description
        payment.capture = False

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

        ## When we add a method we authorize the payment contrary to the v1 api
        assert payment.send() == payment
        assert payment.method == 'card'
        assert card.id is not None
        assert card.id.startswith('card_')
        assert payment.status == PaymentStatus.AUTHORIZED

        # Let's try a capture

        payment.status = PaymentStatus.CAPTURE

        assert payment.send() == payment
        assert payment.status == PaymentStatus.TO_CAPTURE

    @pytest.mark.parametrize('currency', FunctionalTestHelper.currency_provider())
    @pytest.mark.parametrize('version', FunctionalTestHelper.version_provider())
    def test_send_with_unique_id(self, currency, version):
        obj = Payment()
        self.conf.version = version

        amount = self.random_integer(50, 10000)
        desc = f'Python {platform.python_version()} automatic test for `unique_id`, {amount / 100:.2f} {currency.upper()}'
        unique_id = uuid.uuid4()

        card = Card()
        card.number = self.get_card_number()
        card.exp_month = self.random_integer(1, 12)
        card.exp_year = self.random_year()
        card.cvc = str(self.random_integer(100, 999))

        customer = Customer()
        customer.name = 'John Doe'
        customer.email = f'john.doe+{unique_id}@example.com'

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
