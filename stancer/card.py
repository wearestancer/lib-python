# -*- coding: utf-8 -*-

import re
from typing import Optional
from typing import TypeVar

from .core import AbstractCountry
from .core import AbstractLast4
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

CurrentInstance = TypeVar('CurrentInstance', bound='Card')


class Card(AbstractObject, AbstractName, AbstractCountry, AbstractLast4):
    """Representation of a card."""

    _ENDPOINT = 'cards'

    _allowed_attributes = [
        'cvc',
        'exp_month',
        'exp_year',
        'number',
        'tokenize',
        'zip_code',
    ]
    _repr_ignore = {'number'}

    @property
    @populate_on_call
    def brand(self) -> str:
        """
        Card brand.

        Returns:
            Brand code as viewed by the API.
        """
        return self._data.get('brand')

    @property
    def brandname(self) -> str:
        """
        Return real brand name.

        Whereas `Card.brand` returns brand as a simple normalized
        string like "amex",  `Card.brandname` will return a complete
        and real brand name, like "American Express".

        Returns:
            Brand name if known or brand code returned by `Card.brand`.
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
    def cvc(self) -> str:
        """
        Card Verification Code.

        We use string for CVC to prevent errors with leading zeros.

        Args:
            value: New value for CVC.

        Returns:
            Card Verification code.

        Raises:
            InvalidCardVerificationCodeError: When the CVC is invalid.
        """
        return self._data.get('cvc')

    @cvc.setter
    @validate_type(
        str,
        length=3,
        name='CVC',
        throws=InvalidCardVerificationCodeError,
    )
    def cvc(self, value: str):
        self._data['cvc'] = value

    @property
    @populate_on_call
    def exp_month(self) -> int:
        """
        Expiration month.

        Args:
            value: Must be an integer (between 1 and 12).

        Returns:
            Card expiration month.

        Raises:
            InvalidCardExpirationMonthError: When the expiration month is invalid.
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
    def exp_month(self, value: int):
        self._data['exp_month'] = value

    @property
    @populate_on_call
    def exp_year(self) -> int:
        """
        Expiration year.

        Args:
            value: Must be at least equal to the current year.

        Returns:
            Card expiration year.

        Raises:
            InvalidCardExpirationYearError: When the expiration year is invalid.
        """
        return self._data.get('exp_year')

    @exp_year.setter
    @validate_type(
        int,
        name='Expiration year',
        throws=InvalidCardExpirationYearError,
    )
    def exp_year(self, value: int):
        self._data['exp_year'] = value

    @property
    @populate_on_call
    def funding(self) -> Optional[str]:
        """
        Type of funding.

        Should be one of "credit", "debit", "prepaid", "universal", "charge", "deferred".
        May be `None` when the type could not be determined.

        Returns:
            Type of funding.
        """
        return self._data.get('funding')

    @property
    def is_complete(self) -> bool:
        """
        Indicate if all mandatory card data are provided.

        Returns:
            Is the card complete ?
        """
        if self.id is not None:
            return True

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
    @populate_on_call
    def nature(self) -> Optional[str]:
        """
        Nature of the card.

        Should be "personnal" or "corporate".
        May be `None` when the type could not be determined.

        Returns:
            Nature of the card.
        """
        return self._data.get('nature')

    @property
    @populate_on_call
    def network(self) -> Optional[str]:
        """
        Card network.

        Should be "mastercard", "national" or "visa".
        May be `None` when the type could not be determined.

        Returns:
            Card network.
        """
        return self._data.get('network')

    @property
    @populate_on_call
    def number(self) -> str:
        """
        Card number.

        Args:
            value: New card number.

        Returns:
            Card number.

        Raises:
            InvalidCardNumberError: When the card number is invalid.
        """
        return self._data.get('number')

    @number.setter
    @validate_type(str, throws=InvalidCardNumberError)
    def number(self, value: str):
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
            message = f'"{number}" is not a valid credit card number.'
            raise InvalidCardNumberError(message)

        self._data['number'] = number
        self._data['last4'] = number[-4:]

    @property
    @populate_on_call
    def tokenize(self) -> CurrentInstance:
        """
        Indicate if the card can be reuse later.

        Args:
            value: `True` allow reuse, `False` won't.

        Returns:
            Tokenize status.

        Raises:
            InvalidCardTokenizeError: When the token is invalid (should never occur).
        """
        return self._data.get('tokenize')

    @tokenize.setter
    @validate_type(bool, throws=InvalidCardTokenizeError)
    def tokenize(self, value: bool):
        self._data['tokenize'] = value

    @property
    @populate_on_call
    def zip_code(self) -> str:
        """
        City zip code.

        Args:
            value: New zip code, must be between 2 and 8 characters.

        Returns:
            City zip code.

        Raises:
            InvalidZipCodeError: When the zip code is invalid.
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
    def zip_code(self, value: str):
        self._data['zip_code'] = value
