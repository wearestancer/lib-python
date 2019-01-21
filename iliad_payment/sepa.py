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

import re

from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidBicError
from .exceptions import InvalidIbanError


class Sepa(AbstractObject, AbstractName):
    """Representation of a SEPA account."""

    _filtered_attributes = [
        'country',
    ]

    @property
    @populate_on_call
    def bic(self):
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
    def bic(self, value):
        if len(value) != 8 and len(value) != 11:
            # Poorly test but I have nothing more to test
            raise InvalidBicError('"{}" is not a valid BIC.'.format(value))

        self._data['bic'] = value

    @property
    @populate_on_call
    def country(self):
        """
        Account country.

        Returns:
            str: Two characters country code (ISO 3166-1 alpha-2).
        """
        return self._data.get('country')

    @property
    def formatted_iban(self):
        """
        IBAN in readeable format.

        Aka AAAA BBBB CCCC ...

        Returns:
            str: Formatted IBAN.
        """
        iban = self.iban

        if iban is None:
            return None

        return re.sub(r'(.{,4})', '\\1 ', iban).strip()

    @property
    @populate_on_call
    def iban(self):
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
    def iban(self, value):
        iban = re.sub(r'\s', '', value).upper()
        code = ''

        for letter in list(iban[4:] + iban[0:4]):
            if not letter.isnumeric():
                code += str(ord(letter) - 55)
            else:
                code += letter

        if int(code) % 97 != 1:
            raise InvalidIbanError('"{}" is not a valid IBAN.'.format(value))

        self._data['iban'] = iban
        self._data['last4'] = iban[-4:]
        self._data['country'] = iban[0:2].lower()

    @property
    def is_complete(self):
        """
        Indicate if all mandatory data are provided.

        Returns:
            bool: Is the SEPA account complete ?
        """
        if self.bic is None:
            return False

        if self.iban is None:
            return False

        return True

    @property
    def is_not_complete(self):
        """
        Indicate if all mandatory data are NOT provided.

        It's simply a `not self.is_complete`.

        Returns:
            bool: Is the SEPA account not complete ?
        """
        return not self.is_complete

    @property
    @populate_on_call
    def last4(self):
        """
        IBAN's last 4 digits.

        Returns:
            str: IBAN's last 4 digits.
        """
        return self._data.get('last4')
