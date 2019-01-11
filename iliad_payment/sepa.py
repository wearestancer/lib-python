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


class Sepa(AbstractObject, AbstractName):
    """Representation of a SEPA account."""

    _filtered_attributes = [
        'country',
    ]

    @property
    def bic(self):
        """
        Bank Identifier Code.

        Also called SWIFT code.
        """
        return self._data.get('bic', None)

    @bic.setter
    def bic(self, value):
        if not isinstance(value, str):
            raise TypeError('BIC must be a string')

        if len(value) != 8 and len(value) != 11:
            # Poorly test but I have nothing more to test
            raise TypeError('"{}" is not a valid BIC'.format(value))

        self._data['bic'] = value

    @property
    def country(self):
        """Card country."""
        return self._data.get('country', None)

    @property
    def formatted_iban(self):
        """
        Return IBAN with usual readeable format.

        Aka AAAA BBBB CCCC ...
        """
        iban = self.iban

        if iban is None:
            return None

        return re.sub(r'(.{,4})', '\\1 ', iban).strip()

    @property
    def iban(self):
        """
        International Bank Account Number.

        IBAN will be sanitize on update, you may use `formatted_iban`
        to get an human readable number, with 4 characters length blocs
        seperated with spaces.
        """
        return self._data.get('iban', None)

    @iban.setter
    def iban(self, value):
        if not isinstance(value, str):
            raise TypeError('IBAN must be a string')

        iban = re.sub(r'\s', '', value).upper()
        code = ''

        for letter in list(iban[4:] + iban[0:4]):
            if not letter.isnumeric():
                code += str(ord(letter) - 55)
            else:
                code += letter

        if int(code) % 97 != 1:
            raise TypeError('"{}" is not a valid IBAN'.format(value))

        self._data['iban'] = iban
        self._data['last4'] = iban[-4:]
        self._data['country'] = iban[0:2].lower()

    @property
    def last4(self):
        """
        IBAN's last 4 digit.

        Will be a 4 characters lenght string.
        """
        iban = self.iban

        if iban is None:
            return None

        return iban[-4:]
