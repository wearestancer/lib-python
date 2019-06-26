# -*- coding: utf-8 -*-

from builtins import int
from builtins import str

from .decorators import populate_on_call
from .decorators import validate_type
from ..exceptions import InvalidAmountError
from ..exceptions import InvalidCurrencyError


class AbstractAmount(object):  # pylint: disable=too-few-public-methods
    """Common amount management."""

    _allowed_attributes = [
        'amount',
        'currency',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def amount(self):
        """
        Payment or refund amount.

        Must be a an integer and at least 50.
        """
        return self._data.get('amount')

    @amount.setter
    @validate_type(int, min=50, throws=InvalidAmountError)
    def amount(self, value):
        self._data['amount'] = value

    @property
    @populate_on_call
    def currency(self):
        """
        Payment or refund currency.

        Must be one of the following items: eur, gbp, usd
        """
        return self._data.get('currency')

    @currency.setter
    @validate_type(
        str,
        allowed=['eur', 'gbp', 'usd'],
        lowercase=True,
        throws=InvalidCurrencyError,
    )
    def currency(self, value):
        self._data['currency'] = value
