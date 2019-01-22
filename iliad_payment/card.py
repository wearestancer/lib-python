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

from .core import AbstractCountry
from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidCardVerificationCodeError
from .exceptions import InvalidCardExpirationMonthError
from .exceptions import InvalidCardExpirationYearError
from .exceptions import InvalidCardNumberError
from .exceptions import InvalidCardTokenizeError
from .exceptions import InvalidZipCodeError


class Card(AbstractObject, AbstractName, AbstractCountry):
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
        return self._data.get('brand')

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
    def cvc(self):
        """
        Card Verification Code.

        We use string for CVC to prevent errors with leading zeros.

        Args:
            value (str): New value for CVC.

        Returns:
            str: Card Verification code.
        """
        return self._data.get('cvc')

    @cvc.setter
    @validate_type(
        str,
        length=3,
        name='CVC',
        throws=InvalidCardVerificationCodeError,
    )
    def cvc(self, value):
        self._data['cvc'] = value

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
        return self._data.get('exp_month')

    @exp_month.setter
    @validate_type(
        int,
        min=1,
        max=12,
        name='Expiration month',
        throws=InvalidCardExpirationMonthError,
    )
    def exp_month(self, value):
        self._data['exp_month'] = value

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
        return self._data.get('exp_year')

    @exp_year.setter
    @validate_type(
        int,
        min=date.today().year,
        name='Expiration year',
        throws=InvalidCardExpirationYearError,
    )
    def exp_year(self, value):
        self._data['exp_year'] = value

    @property
    def is_complete(self):
        """
        Indicate if all mandatory card data are provided.

        Returns:
            bool: Is the card complete ?
        """
        if self.cvc is None:
            return False

        if self.exp_month is None:
            return False

        if self.exp_year is None:
            return False

        if self.number is None:
            return False

        return True

    @property
    def is_not_complete(self):
        """
        Indicate if all mandatory card data are NOT provided.

        It's simply a `not self.is_complete`.

        Returns:
            bool: Is the card not complete ?
        """
        return not self.is_complete

    @property
    @populate_on_call
    def last4(self):
        """
        Card number's last 4 digits.

        Returns:
            str: Card's last 4 digits.
        """
        return self._data.get('last4')

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
        return self._data.get('number')

    @number.setter
    @validate_type(str, throws=InvalidCardNumberError)
    def number(self, value):
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
            message = '"{}" is not a valid credit card number.'.format(number)
            raise InvalidCardNumberError(message)

        self._data['number'] = number
        self._data['last4'] = number[-4:]

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
        return self._data.get('tokenize')

    @tokenize.setter
    @validate_type(bool, throws=InvalidCardTokenizeError)
    def tokenize(self, value):
        self._data['tokenize'] = value

    @property
    @populate_on_call
    def zip_code(self):
        """
        City zip code.

        Args:
            value (str): New zip code, must be between 2 and 8 characters.

        Returns:
            str: City zip code.
        """
        return self._data.get('zip_code')

    @zip_code.setter
    @validate_type(
        str,
        min=2,
        max=8,
        name='Zip code',
        throws=InvalidZipCodeError,
    )
    def zip_code(self, value):
        self._data['zip_code'] = value
