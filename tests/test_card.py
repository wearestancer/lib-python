"""Test card object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
from datetime import date
import pytest

from iliad_payment import Card
from iliad_payment.core import AbstractObject, AbstractName
from .TestHelper import TestHelper


class TestCard(TestHelper):
    def test_class(self):
        assert issubclass(Card, AbstractObject)
        assert issubclass(Card, AbstractName)

        assert Card._filtered_attributes == [
            'brand',
            'country',
        ]

    def test_id(self):
        assert Card().id is None

        id = self.random_string(29)
        obj = Card(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_brand(self):
        obj = Card()

        assert obj.brand is None

        with pytest.raises(AttributeError):
            obj.brand = self.random_string(15)

    def test_country(self):
        obj = Card()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)

    def test_cvc(self):
        obj = Card()
        cvc = self.random_string(3)

        assert obj.cvc is None

        obj.cvc = cvc

        assert obj.cvc == cvc

        with pytest.raises(TypeError, match='CVC must have 3 characters'):
            obj.cvc = self.random_string(2)

        with pytest.raises(TypeError, match='CVC must be a string'):
            obj.cvc = self.random_integer(1, 100)

    def test_exp_month(self):
        obj = Card()
        exp_month = self.random_integer(1, 12)

        assert obj.exp_month is None

        obj.exp_month = exp_month

        assert obj.exp_month == exp_month

        with pytest.raises(
            TypeError,
            match='Expiration month must be an integer',
        ):
            obj.exp_month = self.random_string(2)

        with pytest.raises(
            TypeError,
            match='Expiration month must be between 1 and 12',
        ):
            obj.exp_month = self.random_integer(13, 100)

        with pytest.raises(
            TypeError,
            match='Expiration month must be between 1 and 12',
        ):
            obj.exp_month = 0

        with pytest.raises(
            TypeError,
            match='Expiration month must be between 1 and 12',
        ):
            obj.exp_month = self.random_integer(1, 12) * -1

    def test_exp_year(self):
        obj = Card()
        current_year = date.today().year
        exp_year = self.random_integer(0, 20) + current_year

        assert obj.exp_year is None

        obj.exp_year = exp_year

        assert obj.exp_year == exp_year

        with pytest.raises(
            TypeError,
            match='Expiration year must be an integer',
        ):
            obj.exp_year = self.random_string(0, 2)

        with pytest.raises(
            TypeError,
            match='Expiration year must be at least the current year',
        ):
            obj.exp_year = current_year - 1

    def test_last4(self):
        obj = Card()

        assert obj.last4 is None

        with pytest.raises(AttributeError):
            obj.last4 = self.random_string(4)

    @pytest.mark.parametrize('number', TestHelper.card_number_provider())
    def test_number(self, number):
        obj = Card()
        last4 = number[-4:]

        assert obj.number is None

        obj.number = number

        assert obj.number == number
        assert obj.last4 == last4

        with pytest.raises(
            TypeError,
            match='Number must be a string',
        ):
            obj.number = self.random_integer(10000)

        bad_number = str(int(number) + 1)

        with pytest.raises(
            TypeError,
            match='{} is not a valid credit card number'.format(bad_number),
        ):
            obj.number = bad_number

    def test_tokenize(self):
        obj = Card()

        assert obj.tokenize is None

        obj.tokenize = True

        assert obj.tokenize is True

        obj.tokenize = False

        assert obj.tokenize is False

        with pytest.raises(
            TypeError,
            match='You should pass a boolean',
        ):
            obj.tokenize = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='You should pass a boolean',
        ):
            obj.tokenize = self.random_string(20)

    def test_to_json(self):
        obj = Card()

        params = {
            'brand': self.random_string(15),
            'country': self.random_string(2),
            'name': self.random_string(4, 64),
            'number': '4242424242424242',
            'exp_month': self.random_integer(1, 12),
            'exp_year': self.random_integer(0, 20) + date.today().year,
            'created': 1546867615,
        }

        obj.hydrate(params)

        result = obj.to_json()

        assert isinstance(result, str)

        assert result.find('"name":"{}"'.format(params['name'])) > 0
        assert result.find('"number":"{}"'.format(params['number'])) > 0
        assert result.find('"exp_month":{}'.format(params['exp_month'])) > 0
        assert result.find('"exp_year":{}'.format(params['exp_year'])) > 0

        assert result.find('brand') == -1
        assert result.find('country') == -1
        assert result.find('created') == -1
        assert result.find('last4') == -1
