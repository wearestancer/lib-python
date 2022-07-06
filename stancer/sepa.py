# -*- coding: utf-8 -*-

from datetime import datetime
import re
from typing import Union

from .core import AbstractCountry
from .core import AbstractLast4
from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidBicError
from .exceptions import InvalidIbanError
from .exceptions import InvalidDateMandateError
from .exceptions import InvalidMandateError


class Sepa(AbstractObject, AbstractName, AbstractCountry, AbstractLast4):
    """Representation of a SEPA account."""

    _ENDPOINT = 'sepa'

    _allowed_attributes = [
        'bic',
        'iban',
    ]
    _datetime_property = [
        'date_mandate',
    ]
    _repr_ignore = {'iban'}

    @property
    @populate_on_call
    def bic(self) -> str:
        """
        Bank Identifier Code.

        Also called SWIFT code.

        Args:
            value (str): New BIC.

        Returns:
            str: BIC.
        """
        return self._data.get('bic')

    @bic.setter
    @validate_type(str, name='BIC', throws=InvalidBicError)
    def bic(self, value: str):
        if len(value) != 8 and len(value) != 11:
            # Poorly test but I have nothing more to test
            raise InvalidBicError(f'"{value}" is not a valid BIC.')

        self._data['bic'] = value

    @property
    @populate_on_call
    def date_mandate(self) -> datetime:
        """
        Mandate signature date.

        Args:
            valuz (datetime|int): New date. Maybe be a datetime object or a timestamp.

        Returns:
            datetime: Mandate signature date.
        """
        return self._data.get('date_mandate')

    @date_mandate.setter
    @validate_type(datetime, throws=InvalidDateMandateError)
    def date_mandate(self, value: Union[int, datetime]):
        self._data['date_mandate'] = value

    @property
    def formatted_iban(self) -> str:
        """
        IBAN in readeable format.

        Aka "FRAA BBBB CCCC DDDD EEEE FFFF GGG" for a french account.

        Returns:
            str: Formatted IBAN.
        """
        iban = self.iban

        if iban is None:
            return None

        return re.sub(r'(.{,4})', '\\1 ', iban).strip()

    @property
    @populate_on_call
    def iban(self) -> str:
        """
        International Bank Account Number.

        IBAN will be sanitize on update, you may use `formatted_iban`
        to get an human readable number, with 4 characters length blocs
        seperated with spaces.

        Args:
            value (str): New IBAN.

        Returns:
            str: Sanitized IBAN.
        """
        return self._data.get('iban')

    @iban.setter
    @validate_type(str, name='IBAN', throws=InvalidIbanError)
    def iban(self, value: str):
        iban = re.sub(r'\s', '', value).upper()
        code = ''

        for letter in list(iban[4:] + iban[0:4]):
            if not letter.isnumeric():
                code += str(ord(letter) - 55)
            else:
                code += letter

        if int(code) % 97 != 1:
            raise InvalidIbanError(f'"{value}" is not a valid IBAN.')

        self._data['iban'] = iban
        self._data['last4'] = iban[-4:]
        self._data['country'] = iban[0:2].lower()

    @property
    def is_complete(self) -> bool:
        """
        Indicate if all mandatory data are provided.

        Returns:
            Is the SEPA account complete ?
        """
        if self.id is not None:
            return True

        if self.bic is None:
            return False

        if self.iban is None:
            return False

        return True

    @property
    @populate_on_call
    def mandate(self) -> str:
        """
        Referring mandate.

        Args:
            value (str): New mandate.

        Returns:
            str: Mandate.
        """
        return self._data.get('mandate')

    @mandate.setter
    @validate_type(str, min=3, max=35, throws=InvalidMandateError)
    def mandate(self, value: str):
        self._data['mandate'] = value
