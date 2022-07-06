"""Test sepa object"""

from datetime import datetime
from datetime import timezone
from datetime import tzinfo
import pytest
from pytz import timezone as tz
import re
import responses

from stancer import Config
from stancer import Sepa
from stancer.core import AbstractCountry
from stancer.core import AbstractObject
from stancer.core import AbstractName
from stancer.exceptions import InvalidBicError
from stancer.exceptions import InvalidDateMandateError
from stancer.exceptions import InvalidIbanError
from stancer.exceptions import InvalidMandateError
from .TestHelper import TestHelper


class TestSepa(TestHelper):
    def test_class(self):
        assert issubclass(Sepa, AbstractCountry)
        assert issubclass(Sepa, AbstractName)
        assert issubclass(Sepa, AbstractObject)

    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test__repr(self, iban):
        obj = Sepa()

        assert repr(obj) == '<Sepa() at 0x%x>' % id(obj)

        obj = Sepa(**{ 'iban': iban })

        spaceless = re.sub(r'\s', '', iban)

        params = {
            'country': spaceless[0:2].lower(),
            'id': id(obj),
            'last4': spaceless[-4:],
        }

        assert repr(obj) == '<Sepa(country="{country}", last4="{last4}") at 0x{id:x}>'.format(**params)

    @responses.activate
    def test_bic(self):
        obj = Sepa()
        bic = self.random_string(8)

        assert obj.bic is None
        assert obj.is_not_modified

        obj.bic = bic

        assert obj.bic == bic
        assert obj.is_modified

        with pytest.raises(
            InvalidBicError,
            match='BIC must be a string.',
        ):
            obj.bic = self.random_integer(20)

        bad_bic = self.random_string(15)

        with pytest.raises(
            InvalidBicError,
            match='"{}" is not a valid BIC'.format(bad_bic),
        ):
            obj.bic = bad_bic

        obj = Sepa(self.random_string(29))
        params = {
            'bic': self.random_string(11),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.bic == params['bic']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_country(self):
        obj = Sepa()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)

        obj = Sepa(self.random_string(29))
        params = {
            'country': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.country == params['country']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_date_mandate(self):
        obj = Sepa()
        timestamp = self.random_integer(1_500_000_000, 1_600_000_000)
        date = datetime.now()
        config = Config()
        zone = 'Europe/Paris'

        assert obj.date_mandate is None

        obj.date_mandate = timestamp

        assert isinstance(obj.date_mandate, datetime)
        assert obj.date_mandate.timestamp() == timestamp
        assert obj.date_mandate.tzinfo is timezone.utc

        obj.date_mandate = date

        assert isinstance(obj.date_mandate, datetime)
        assert obj.date_mandate == date

        config.default_timezone = tz(zone)

        obj.date_mandate = timestamp

        assert isinstance(obj.date_mandate, datetime)
        assert obj.date_mandate.timestamp() == timestamp
        assert isinstance(obj.date_mandate.tzinfo, tzinfo)
        assert obj.date_mandate.tzinfo.zone == zone

        with pytest.raises(
            InvalidDateMandateError,
            match='You must provide a valid instance of datetime.',
        ):
            obj.date_mandate = self.random_string(2)

        obj = Sepa(self.random_string(29))
        params = {
            'date_mandate': self.random_integer(1_500_000_000, 1_600_000_000),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.date_mandate, datetime)
        assert obj.date_mandate.timestamp() == params['date_mandate']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test_formatted_iban(self, iban):
        obj = Sepa()

        assert obj.formatted_iban is None

        obj.iban = iban

        spaceless = re.sub(r'\s', '', iban)
        formatted = re.sub(r'(.{,4})', '\\1 ', spaceless).strip()

        assert obj.formatted_iban == formatted

        obj = Sepa(self.random_string(29))
        params = {
            'iban': iban,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.iban == spaceless
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test_iban(self, iban):
        obj = Sepa()

        spaceless = re.sub(r'\s', '', iban)

        assert obj.iban is None
        assert obj.is_not_modified

        obj.iban = iban

        assert obj.iban == spaceless
        assert obj.last4 == spaceless[-4:]
        assert obj.country == spaceless[0:2].lower()
        assert obj.is_modified

        with pytest.raises(
            InvalidIbanError,
            match='IBAN must be a string.',
        ):
            obj.iban = self.random_integer(10000)

        bad_iban = 'FR87BARC20658244971655'

        with pytest.raises(
            InvalidIbanError,
            match='"{}" is not a valid IBAN.'.format(bad_iban),
        ):
            obj.iban = bad_iban

        obj = Sepa(self.random_string(29))
        params = {
            'iban': iban,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.iban == spaceless
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_is_complete(self):
        uid = 'sepa_{}'.format(self.random_string(24))
        bic = self.random_string(8)
        iban = 'GB82WEST12345698765432'

        # Empty SEPA is not complete
        assert Sepa().is_complete is False
        assert Sepa().is_not_complete is True

        # A SEPA with an ID is complete
        obj = Sepa(uid)

        assert obj.is_complete is True
        assert obj.is_not_complete is False

        # Without BIC => incomplete
        obj = Sepa()

        obj.bic = bic
        # obj.iban

        assert obj.is_complete is False
        assert obj.is_not_complete is True

        # Minimum to be complete
        obj = Sepa()

        obj.bic = bic
        obj.iban = iban

        assert obj.is_complete is True
        assert obj.is_not_complete is False

    @responses.activate
    def test_last4(self):
        obj = Sepa()

        assert obj.last4 is None

        with pytest.raises(AttributeError):
            obj.last4 = self.random_string(4)

        obj = Sepa(self.random_string(29))
        params = {
            'last4': self.random_string(4),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.last4 == params['last4']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_mandate(self):
        obj = Sepa()
        mandate = self.random_string(35)

        assert obj.mandate is None

        obj.mandate = mandate

        assert obj.mandate == mandate

        with pytest.raises(
            InvalidMandateError,
            match='Mandate must be a string.',
        ):
            obj.mandate = self.random_integer(20)

        with pytest.raises(
            InvalidMandateError,
            match='Mandate must be between 3 and 35 characters.',
        ):
            obj.mandate = self.random_string(2)

        with pytest.raises(
            InvalidMandateError,
            match='Mandate must be between 3 and 35 characters.',
        ):
            obj.mandate = self.random_string(36)

        obj = Sepa(self.random_string(29))
        params = {
            'mandate': self.random_string(20),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.mandate == params['mandate']
        assert obj.is_populated
        assert len(responses.calls) == 1
