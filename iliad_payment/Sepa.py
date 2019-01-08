# -*- coding: utf-8 -*-

from .core.Object import Object

import re
import string


class Sepa(Object):
    """Representation of a SEPA account."""

    @property
    def bic(self):
        """
        Bank Identifier Code.

        Also called SWIFT code.
        """
        return self._data.get('bic', None)

    @bic.setter
    def bic(self, value):
        if type(value) != str:
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

        if iban is not None:
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
        if type(value) != str:
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

        if iban is not None:
            return iban[-4:]

    @property
    def name(self):
        """
        Card holder name.

        Must be a string between 4 and 64 characters.
        """
        return self._data.get('name', None)

    @name.setter
    def name(self, value):
        if type(value) != str:
            raise TypeError('Name must be a string')

        if len(value) < 4 or len(value) > 64:
            message = 'Name must be have at between 4 and 64 characters'
            raise TypeError(message)

        self._data['name'] = value
