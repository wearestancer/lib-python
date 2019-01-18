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

from .decorators import populate_on_call
from .decorators import validate_type


class AbstractAmount(object):  # pylint: disable=too-few-public-methods
    """Common amount management."""

    def __init__(self):
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
    @validate_type(int, min=50)
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
    @validate_type(str, allowed=['eur', 'gbp', 'usd'], lowercase=True)
    def currency(self, value):
        self._data['currency'] = value
