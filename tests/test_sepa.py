"""Test sepa object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from future import standard_library
standard_library.install_aliases()

import pytest
import re
import responses

from iliad_payment import Sepa
from iliad_payment.core import AbstractObject, AbstractName
from iliad_payment.exceptions import InvalidBicError
from iliad_payment.exceptions import InvalidIbanError
from .TestHelper import TestHelper


class TestSepa(TestHelper):
    def test_class(self):
        assert issubclass(Sepa, AbstractObject)
        assert issubclass(Sepa, AbstractName)

        attrs = Sepa._get_filtered_attributes()

        assert isinstance(attrs, list)
        assert 'country' in attrs
        assert 'created' in attrs
        assert 'id' in attrs

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
    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test_formatted_iban(self, iban):
        obj = Sepa()

        assert obj.formatted_iban is None

        obj.iban = iban

        spaceless = re.sub(r'\s', '', iban)
        formatted = re.sub(r'(.{,4})', '\\1 ', spaceless)

        assert obj.formatted_iban == formatted.strip()

        obj = Sepa(self.random_string(29))
        params = {
            'iban': iban,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.iban == iban
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test_iban(self, iban):
        obj = Sepa()
        formatted = re.sub(r'\s', '', iban)

        assert obj.iban is None
        assert obj.is_not_modified

        obj.iban = iban

        assert obj.iban == formatted
        assert obj.last4 == formatted[-4:]
        assert obj.country == formatted[0:2].lower()
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

        assert obj.iban == iban
        assert obj.is_populated
        assert len(responses.calls) == 1

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
