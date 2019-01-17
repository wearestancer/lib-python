# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import


class AbstractAmount(object):  # pylint: disable=too-few-public-methods
    """Common amount management."""

    _allowed_currencies = ('eur', 'gbp', 'usd')

    def __init__(self):
        self._data = {}

    @property
    def amount(self):
        """
        Payment or refund amount.

        Must be a an integer and at least 50.
        """
        return self._data.get('amount')

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise TypeError('Amount must be an integer')

        if value < 50:
            tmp = 'Amount must be greater than or equal to 50'

            raise TypeError(tmp.format('Amount', 4, 64))

        self._data['amount'] = value
        self._modified = True

    @property
    def currency(self):
        """
        Payment or refund currency.

        Must be one of the following items: eur, gbp, usd
        """
        return self._data.get('currency')

    @currency.setter
    def currency(self, value):
        if not isinstance(value, str):
            raise TypeError('Currency must be a string')

        currency = value.lower()

        if currency not in self._allowed_currencies:
            message = '{} is not a valid currency,'\
                'please use one of following: {}'\
                .format(value, ', '.join(self._allowed_currencies))
            raise TypeError(message)

        self._data['currency'] = currency
        self._modified = True
