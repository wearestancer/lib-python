"""Test payment object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment import Payment, Card, Customer, Sepa
from iliad_payment.core import AbstractObject, AbstractAmount
from .TestHelper import TestHelper


class TestPayment(TestHelper):
    def test_class(self):
        assert issubclass(Payment, AbstractObject)
        assert issubclass(Payment, AbstractAmount)

        assert Payment._filtered_attributes == [
            'method',
        ]

    def test_amount(self):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag

        obj = Payment()
        amount = self.random_integer(50, 999999)

        assert obj.is_not_modified

        obj.amount = amount

        assert obj.amount == amount
        assert obj.is_modified

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
            TypeError,
            match='Capture must be a boolean',
        ):
            obj.capture = self.random_integer(2)

        with pytest.raises(
            TypeError,
            match='Capture must be a boolean',
        ):
            obj.capture = self.random_string(2)

    def test_card(self):
        obj = Payment()
        card = Card()

        assert obj.card is None
        assert obj.method is None

        obj.card = card

        assert obj.card == card
        assert obj.method == 'card'

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Card',
        ):
            obj.card = self.random_integer(2)

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Card',
        ):
            obj.card = self.random_string(2)

    def test_customer(self):
        obj = Payment()
        customer = Customer()

        assert obj.customer is None

        obj.customer = customer

        assert obj.customer == customer

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Customer',
        ):
            obj.customer = self.random_integer(2)

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Customer',
        ):
            obj.customer = self.random_string(2)

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_currency(self, currency):
        # More test on test_abstract_amount
        # Here we are just testing the modified flag

        obj = Payment()

        assert obj.is_not_modified

        obj.currency = currency

        assert obj.currency == currency
        assert obj.is_modified

    def test_description(self):
        obj = Payment()
        description = self.random_string(3, 64)

        assert obj.description is None

        obj.description = description

        assert obj.description == description

        with pytest.raises(
            TypeError,
            match='Description must be a string',
        ):
            obj.description = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='A valid description must be between 3 and 64 characters',
        ):
            obj.description = self.random_string(2)

        with pytest.raises(
            TypeError,
            match='A valid description must be between 3 and 64 characters',
        ):
            obj.description = self.random_string(65)

    def test_method(self):
        obj = Payment()

        assert obj.method is None

        with pytest.raises(AttributeError):
            obj.method = self.random_string(29)

    def test_order_id(self):
        obj = Payment()
        order_id = self.random_string(1, 24)

        assert obj.order_id is None

        obj.order_id = order_id

        assert obj.order_id == order_id

        with pytest.raises(
            TypeError,
            match='Order id must be a string',
        ):
            obj.order_id = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='Order id must have maximum 24 characters',
        ):
            obj.order_id = self.random_string(25, 30)

    def test_response_code(self):
        obj = Payment()

        assert obj.response_code is None

        with pytest.raises(AttributeError):
            obj.response_code = self.random_string(29)

    def test_response_message(self):
        obj = Payment()

        assert obj.response_message is None

        with pytest.raises(AttributeError):
            obj.response_message = self.random_string(29)

    def test_sepa(self):
        obj = Payment()
        sepa = Sepa()

        assert obj.sepa is None
        assert obj.method is None

        obj.sepa = sepa

        assert obj.sepa == sepa
        assert obj.method == 'sepa'

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Sepa',
        ):
            obj.sepa = self.random_integer(2)

        with pytest.raises(
            TypeError,
            match='You must provide a valid instance of Sepa',
        ):
            obj.sepa = self.random_string(2)

    def test_status(self):
        obj = Payment()

        assert obj.status is None

        with pytest.raises(AttributeError):
            obj.status = self.random_string(29)

    def test_uri(self):
        obj = Payment()
        uid = self.random_string(29)

        assert obj.uri == 'https://api.iliad78.net/v1/checkout'

        obj.hydrate({'id': uid})

        assert obj.uri == 'https://api.iliad78.net/v1/checkout/' + uid

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
