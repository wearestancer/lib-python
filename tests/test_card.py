"""Test card object"""

import pytest
import responses

from stancer import Card
from stancer.core import AbstractCountry
from stancer.core import AbstractObject
from stancer.core import AbstractName
from stancer.exceptions import InvalidCardVerificationCodeError
from stancer.exceptions import InvalidCardExpirationMonthError
from stancer.exceptions import InvalidCardExpirationYearError
from stancer.exceptions import InvalidCardNumberError
from stancer.exceptions import InvalidCardTokenizeError
from stancer.exceptions import InvalidZipCodeError
from .TestHelper import TestHelper


class TestCard(TestHelper):
    def test_class(self):
        assert issubclass(Card, AbstractCountry)
        assert issubclass(Card, AbstractName)
        assert issubclass(Card, AbstractObject)

    @pytest.mark.parametrize('number', TestHelper.card_number_provider())
    def test__repr(self, number):
        obj = Card()

        assert repr(obj) == '<Card() at 0x%x>' % id(obj)

        obj = Card(**{'number': number})

        params = {
            'id': id(obj),
            'last4': number[-4:]
        }

        assert repr(obj) == '<Card(last4="{last4}") at 0x{id:x}>'.format(**params)

    def test_id(self):
        assert Card().id is None

        uid = self.random_string(29)
        obj = Card(uid)

        assert obj.id == uid

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    @responses.activate
    def test_brand(self):
        obj = Card()

        assert obj.brand is None

        with pytest.raises(AttributeError):
            obj.brand = self.random_string(15)

        obj = Card(self.random_string(29))
        params = {
            'brand': self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.brand == params['brand']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize('brand', TestHelper.card_brand_provider())
    def test_brandname(self, brand):
        obj = Card(self.random_string(29))

        params = {
            'brand': brand[0],
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.brandname == brand[1]
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_country(self):
        obj = Card()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)

        obj = Card(self.random_string(29))
        params = {
            'country': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.country == params['country']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_cvc(self):
        obj = Card()
        cvc = self.random_string(3)

        assert obj.cvc is None
        assert obj.is_not_modified

        obj.cvc = cvc

        assert obj.cvc == cvc
        assert obj.is_modified

        with pytest.raises(
            InvalidCardVerificationCodeError,
            match='CVC must have 3 characters.',
        ):
            obj.cvc = self.random_string(2)

        with pytest.raises(
            InvalidCardVerificationCodeError,
            match='CVC must be a string.',
        ):
            obj.cvc = self.random_integer(1, 100)

        obj = Card(self.random_string(29))
        params = {
            'cvc': self.random_string(3),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.cvc == params['cvc']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_exp_month(self):
        obj = Card()
        exp_month = self.random_integer(1, 12)

        assert obj.exp_month is None
        assert obj.is_not_modified

        obj.exp_month = exp_month

        assert obj.exp_month == exp_month
        assert obj.is_modified

        with pytest.raises(
            InvalidCardExpirationMonthError,
            match='Expiration month must be an integer.',
        ):
            obj.exp_month = self.random_string(2)

        with pytest.raises(
            InvalidCardExpirationMonthError,
            match='Expiration month must be between 1 and 12.',
        ):
            obj.exp_month = self.random_integer(13, 100)

        with pytest.raises(
            InvalidCardExpirationMonthError,
            match='Expiration month must be between 1 and 12.',
        ):
            obj.exp_month = 0

        with pytest.raises(
            InvalidCardExpirationMonthError,
            match='Expiration month must be between 1 and 12.',
        ):
            obj.exp_month = self.random_integer(1, 12) * -1

        obj = Card(self.random_string(29))
        params = {
            'exp_month': self.random_integer(1, 12),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.exp_month == params['exp_month']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_exp_year(self):
        obj = Card()
        exp_year = self.random_year()

        assert obj.exp_year is None
        assert obj.is_not_modified

        obj.exp_year = exp_year

        assert obj.exp_year == exp_year
        assert obj.is_modified

        with pytest.raises(
            InvalidCardExpirationYearError,
            match='Expiration year must be an integer.',
        ):
            obj.exp_year = self.random_string(4)

        obj = Card(self.random_string(29))
        params = {
            'exp_year': self.random_year(),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.exp_year == params['exp_year']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_funding(self):
        obj = Card()

        assert obj.funding is None

        with pytest.raises(AttributeError):
            obj.funding = self.random_string(15)

        obj = Card(self.random_string(29))
        params = {
            'funding': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.funding == params['funding']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_is_complete(self):
        uid = 'card_{}'.format(self.random_string(24))
        cvc = self.random_string(3)
        exp_month = self.random_integer(1, 12)
        exp_year = self.random_year()
        number = '4242424242424242'

        # Empty card is not complete
        assert Card().is_complete is False
        assert Card().is_not_complete is True

        # A card with an ID is complete
        obj = Card(uid)

        assert obj.is_complete is True
        assert obj.is_not_complete is False

        # Without CVC => incomplete
        obj = Card()

        # obj.cvc
        obj.exp_month = exp_month
        obj.exp_year = exp_year
        obj.number = number

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Without expiration month => incomplete
        obj = Card()

        obj.cvc = cvc
        # obj.exp_month
        obj.exp_year = exp_year
        obj.number = number

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Without expiration year => incomplete
        obj = Card()

        obj.cvc = cvc
        obj.exp_month = exp_month
        # obj.exp_year
        obj.number = number

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Without number => incomplete
        obj = Card()

        obj.cvc = cvc
        obj.exp_month = exp_month
        obj.exp_year = exp_year
        # obj.number

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Minimum to be complete
        obj = Card()

        obj.cvc = cvc
        obj.exp_month = exp_month
        obj.exp_year = exp_year
        obj.number = number

        assert obj.is_complete is True
        assert obj.is_not_complete is False

    @responses.activate
    def test_last4(self):
        obj = Card()

        assert obj.last4 is None

        with pytest.raises(AttributeError):
            obj.last4 = self.random_string(4)

        obj = Card(self.random_string(29))
        params = {
            'last4': self.random_string(4),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.last4 == params['last4']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_nature(self):
        obj = Card()

        assert obj.nature is None

        with pytest.raises(AttributeError):
            obj.nature = self.random_string(15)

        obj = Card(self.random_string(29))
        params = {
            'nature': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.nature == params['nature']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_network(self):
        obj = Card()

        assert obj.network is None

        with pytest.raises(AttributeError):
            obj.network = self.random_string(15)

        obj = Card(self.random_string(29))
        params = {
            'network': self.random_string(10),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.network == params['network']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize('number', TestHelper.card_number_provider())
    def test_number(self, number):
        obj = Card()
        last4 = number[-4:]

        assert obj.number is None
        assert obj.is_not_modified

        obj.number = number

        assert obj.number == number
        assert obj.last4 == last4
        assert obj.is_modified

        with pytest.raises(
            InvalidCardNumberError,
            match='Number must be a string.',
        ):
            obj.number = self.random_integer(10000)

        bad_number = str(int(number) + 1)

        with pytest.raises(
            InvalidCardNumberError,
            match='"{}" is not a valid credit card number.'.format(bad_number),
        ):
            obj.number = bad_number

        obj = Card(self.random_string(29))
        params = {
            'number': number,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.number == params['number']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_tokenize(self):
        obj = Card()

        assert obj.tokenize is None
        assert obj.is_not_modified

        obj.tokenize = True

        assert obj.tokenize is True
        assert obj.is_modified

        obj.tokenize = False

        assert obj.tokenize is False

        with pytest.raises(
            InvalidCardTokenizeError,
            match='Tokenize must be a boolean.',
        ):
            obj.tokenize = self.random_integer(20)

        with pytest.raises(
            InvalidCardTokenizeError,
            match='Tokenize must be a boolean.',
        ):
            obj.tokenize = self.random_string(20)

        obj = Card(self.random_string(29))
        params = {
            'tokenize': True,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.tokenize == params['tokenize']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_to_json(self):
        obj = Card()

        params = {
            'brand': self.random_string(15),
            'country': self.random_string(2),
            'name': self.random_string(4, 64),
            'number': '4242424242424242',
            'exp_month': self.random_integer(1, 12),
            'exp_year': self.random_year(),
            'created': 1546867615,
        }

        obj.hydrate(**params)

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

    @responses.activate
    def test_zip_code(self):
        obj = Card()
        zip_code = self.random_string(2, 8)

        assert obj.zip_code is None
        assert obj.is_not_modified

        obj.zip_code = zip_code

        assert obj.zip_code == zip_code
        assert obj.is_modified

        with pytest.raises(
            InvalidZipCodeError,
            match='Zip code must be a string.',
        ):
            obj.zip_code = self.random_integer(20)

        with pytest.raises(
            InvalidZipCodeError,
            match='Zip code must be between 2 and 8 characters.',
        ):
            obj.zip_code = self.random_string(1)

        with pytest.raises(
            InvalidZipCodeError,
            match='Zip code must be between 2 and 8 characters.',
        ):
            obj.zip_code = self.random_string(9, 10)

        obj = Card(self.random_string(2, 8))
        params = {
            'zip_code': self.random_string(2, 8),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.zip_code == params['zip_code']
        assert obj.is_populated
        assert len(responses.calls) == 1
