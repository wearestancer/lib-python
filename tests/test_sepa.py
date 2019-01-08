"""Test sepa object"""

from iliad_payment import Sepa
from iliad_payment.core import Object
from .TestHelper import TestHelper

import pytest
import re


class TestSepa(TestHelper):
    def test_class(self):
        assert issubclass(Sepa, Object)

    def test_bic(self):
        obj = Sepa()
        bic = self.random_string(8)

        assert obj.bic is None

        obj.bic = bic

        assert obj.bic == bic

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

        obj.iban = iban

        assert obj.iban == formatted
        assert obj.last4 == formatted[-4:]
        assert obj.country == formatted[0:2].lower()

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

    def test_name(self):
        obj = Sepa()
        name = self.random_string(10)

        assert obj.name is None

        obj.name = name

        assert obj.name == name

        with pytest.raises(
            TypeError,
            match='Name must be a string',
        ):
            obj.name = self.random_integer(20)

        with pytest.raises(
            TypeError,
            match='Name must be have at between 4 and 64 characters',
        ):
            obj.name = self.random_string(3)

        with pytest.raises(
            TypeError,
            match='Name must be have at between 4 and 64 characters',
        ):
            obj.name = self.random_string(65, 70)
