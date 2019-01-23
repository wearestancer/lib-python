"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment.core import AbstractAmount
from iliad_payment.exceptions import InvalidAmountError
from iliad_payment.exceptions import InvalidCurrencyError
from ..TestHelper import TestHelper


class TestAbstractAmount(TestHelper):
    def test_amount(self):
        obj = AbstractAmount()
        amount = self.random_integer(50, 999999)

        assert obj.amount is None

        obj.amount = amount

        assert obj.amount == amount

        with pytest.raises(
            InvalidAmountError,
            match='Amount must be an integer.',
        ):
            obj.amount = self.random_string(2)

        with pytest.raises(
            InvalidAmountError,
            match='Amount must be greater than or equal to 50.',
        ):
            obj.amount = self.random_integer(49)

        with pytest.raises(
            InvalidAmountError,
            match='Amount must be greater than or equal to 50.',
        ):
            obj.amount = 0

    @pytest.mark.parametrize('currency', TestHelper.currency_provider())
    def test_currency(self, currency):
        obj = AbstractAmount()

        assert obj.currency is None

        obj.currency = currency

        assert obj.currency == currency

        obj.currency = currency.upper()

        assert obj.currency == currency.lower()

        with pytest.raises(
            InvalidCurrencyError,
            match='Currency must be a string.',
        ):
            obj.currency = self.random_integer(100)

        allowed_currency = ['eur', 'gbp', 'usd']
        bad_currency = self.random_string(3)
        message = (
            '"{}" is not a valid currency, '
            'please use one of following: {}'
        ).format(bad_currency, ', '.join(allowed_currency))

        with pytest.raises(
            InvalidCurrencyError,
            match=message,
        ):
            obj.currency = bad_currency
