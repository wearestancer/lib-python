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

from datetime import date
import re

from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call


class Card(AbstractObject, AbstractName):
    """Representation of a card."""

    _filtered_attributes = [
        'brand',
        'country',
    ]

    @property
    @populate_on_call
    def brand(self):
        """
        Card brand.

        Returns:
            str: Brand code as viewed by the API.
        """
        return self._data.get('brand', None)

    @property
    def brandname(self):
        """
        Return real brand name.

        Whereas `Card.brand` returns brand as a simple normalized
        string like "amex",  `Card.brandname` will return a complete
        and real brand name, like "American Express".

        Returns:
            str: Brand name if known or brand code returned by `Card.brand`.
        """
        brand = self.brand

        names = {
            'visa': 'VISA',
            'mastercard': 'MasterCard',
            'amex': 'American Express',
            'jcb': 'JCB',
            'maestro': 'Maestro',
            'discover': 'Discover',
            'dankort': 'Dankort',
        }

        if brand in names:
            return names[brand]

        return brand

    @property
    @populate_on_call
    def country(self):
        """
        Card country.

        Returns:
            str: Two characters country code (ISO 3166-1 alpha-2).
        """
        return self._data.get('country', None)

    @property
    @populate_on_call
    def cvc(self):
        """
        Card Verification Code.

        We use string for CVC to prevent errors with leading zeros.

        Args:
            value (str): New value for CVC.

        Returns:
            str: Card Verification code.
        """
        return self._data.get('cvc', None)

    @cvc.setter
    def cvc(self, value):
        if not isinstance(value, str):
            raise TypeError('CVC must be a string')

        if len(value) != 3:
            raise TypeError('CVC must have 3 characters')

        self._data['cvc'] = value
        self._modified = True

    @property
    @populate_on_call
    def exp_month(self):
        """
        Expiration month.

        Args:
            value (int): Must be an integer (between 1 and 12).

        Returns:
            int: Card expiration month.
        """
        return self._data.get('exp_month', None)

    @exp_month.setter
    def exp_month(self, value):
        if not isinstance(value, int):
            raise TypeError('Expiration month must be an integer')

        if value < 1 or value > 12:
            raise TypeError('Expiration month must be between 1 and 12')

        self._data['exp_month'] = value
        self._modified = True

    @property
    @populate_on_call
    def exp_year(self):
        """
        Expiration year.

        Args:
            value (int): Must be at least equal to the current year.

        Returns:
            int: Card expiration year.
        """
        return self._data.get('exp_year', None)

    @exp_year.setter
    def exp_year(self, value):
        if not isinstance(value, int):
            raise TypeError('Expiration year must be an integer')

        if value < date.today().year:
            message = 'Expiration year must be at least the current year'
            raise TypeError(message)

        self._data['exp_year'] = value
        self._modified = True

    @property
    @populate_on_call
    def last4(self):
        """
        Card number's last 4 digits.

        Returns:
            str: Card's last 4 digits.
        """
        return self._data.get('last4', None)

    @property
    @populate_on_call
    def number(self):
        """
        Card number.

        Args:
            value (str): New card number.

        Returns:
            str: Card number.
        """
        return self._data.get('number', None)

    @number.setter
    def number(self, value):
        if not isinstance(value, str):
            raise TypeError('Number must be a string')

        number = re.sub(r'\D', '', value)
        parts = list(map(int, number))
        calc = [
            0,
            2,
            4,
            6,
            8,
            1,
            3,
            5,
            7,
            9,
        ]

        parts.reverse()

        chk = [calc[val] if idx % 2 else val for idx, val in enumerate(parts)]

        if sum(chk) % 10:
            message = '{} is not a valid credit card number'.format(number)
            raise TypeError(message)

        self._data['number'] = number
        self._data['last4'] = number[-4:]
        self._modified = True

    @property
    @populate_on_call
    def tokenize(self):
        """
        Indicate if the card can be reuse later.

        Args:
            value (bool): `True` allow reuse, `False` won't.

        Returns:
            bool: Tokenize status.
        """
        return self._data.get('tokenize', None)

    @tokenize.setter
    def tokenize(self, value):
        if not isinstance(value, bool):
            message = 'You should pass a boolean'
            raise TypeError(message)

        self._data['tokenize'] = value
        self._modified = True
