# -*- coding: utf-8 -*-

from .decorators import populate_on_call
from .decorators import validate_type
from ..exceptions import InvalidAmountError
from ..exceptions import InvalidCurrencyError


class AbstractAmount(object):
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
    def amount(self) -> int:
        """
        Payment or refund amount.

        Must be a an integer and at least 50.

        Args:
            value: New amount.

        Returns:
            Current amount.

        Raises:
            InvalidAmountError: When amount is under 50.
        """
        return self._data.get('amount')

    @amount.setter
    @validate_type(int, min=50, throws=InvalidAmountError)
    def amount(self, value: int):
        self._data['amount'] = value

    @property
    @populate_on_call
    def currency(self) -> str:
        """
        Payment or refund currency.

        Must be one of the following items: eur, gbp, usd

        Args:
            value: New currency.

        Returns:
            Current currency.

        Raises:
            InvalidCurrencyError: When currency is not ``eur``, ``gbp`` or ``usd``.
        """
        return self._data.get('currency')

    @currency.setter
    @validate_type(
        str,
        allowed=['eur', 'gbp', 'usd'],
        lowercase=True,
        throws=InvalidCurrencyError,
    )
    def currency(self, value: str):
        self._data['currency'] = value
