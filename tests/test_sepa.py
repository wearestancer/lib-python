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

from iliad_payment import Sepa
from iliad_payment.core import AbstractObject, AbstractName
from .TestHelper import TestHelper


class TestSepa(TestHelper):
    def test_class(self):
        assert issubclass(Sepa, AbstractObject)
        assert issubclass(Sepa, AbstractName)

        assert Sepa._filtered_attributes == [
            'country',
        ]

    def test_bic(self):
        obj = Sepa()
        bic = self.random_string(8)

        assert obj.bic is None
        assert obj.is_not_modified

        obj.bic = bic

        assert obj.bic == bic
        assert obj.is_modified

        with pytest.raises(
            TypeError,
            match='BIC must be a string',
        ):
            obj.bic = self.random_integer(20)

        bad_bic = self.random_string(15)

        with pytest.raises(
            TypeError,
            match='"{}" is not a valid BIC'.format(bad_bic),
        ):
            obj.bic = bad_bic

    def test_country(self):
        obj = Sepa()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)

    @pytest.mark.parametrize('iban', TestHelper.iban_provider())
    def test_formatted_iban(self, iban):
        obj = Sepa()

        assert obj.formatted_iban is None

        obj.iban = iban

        spaceless = re.sub(r'\s', '', iban)
        formatted = re.sub(r'(.{,4})', '\\1 ', spaceless)

        assert obj.formatted_iban == formatted.strip()

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
            TypeError,
            match='IBAN must be a string',
        ):
            obj.iban = self.random_integer(10000)

        bad_iban = 'FR87BARC20658244971655'

        with pytest.raises(
            TypeError,
            match='"{}" is not a valid IBAN'.format(bad_iban),
        ):
            obj.iban = bad_iban

    def test_last4(self):
        obj = Sepa()

        assert obj.last4 is None

        with pytest.raises(AttributeError):
            obj.last4 = self.random_string(4)
