# -*- coding: utf-8 -*-

from .core.Object import Object

from datetime import date
import re


class Card(Object):
    """Representation of a card."""

    @property
    def brand(self):
        """Card brand."""
        return self._data.get('brand', None)

    @property
    def country(self):
        """Card country."""
        return self._data.get('country', None)

    @property
    def cvc(self):
        """
        Card Verification Code.

        We use string for CVC to prevent errors with leading zeros.
        """
        return self._data.get('cvc', None)

    @cvc.setter
    def cvc(self, value):
        if type(value) != str:
            raise TypeError('CVC must be a string')

        if len(value) != 3:
            raise TypeError('CVC must have 3 characters')

        self._data['cvc'] = value

    @property
    def exp_month(self):
        """
        Expiration month.

        Must be an integer (between 1 and 12).
        """
        return self._data.get('exp_month', None)

    @exp_month.setter
    def exp_month(self, value):
        if type(value) != int:
            raise TypeError('Expiration month must be an integer')

        if value < 1 or value > 12:
            raise TypeError('Expiration month must be between 1 and 12')

        self._data['exp_month'] = value

    @property
    def exp_year(self):
        """
        Expiration year.

        Must be an integer (at least equal to the current year).
        """
        return self._data.get('exp_year', None)

    @exp_year.setter
    def exp_year(self, value):
        if type(value) != int:
            raise TypeError('Expiration year must be an integer')

        if value < date.today().year:
            message = 'Expiration year must be at least the current year'
            raise TypeError(message)

        self._data['exp_year'] = value

    @property
    def last4(self):
        """
        Card number's last 4 digit.

        Will be a 4 characters lenght string.
        """
        number = self.number

        if number is not None:
            return number[-4:]

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

    @property
    def number(self):
        """
        Card number.

        Must be a string.
        """
        return self._data.get('number', None)

    @number.setter
    def number(self, value):
        if type(value) != str:
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

    @property
    def tokenize(self):
        """
        Indicate if the card can be reuse later.
        """
        return self._data.get('tokenize', None)

    @tokenize.setter
    def tokenize(self, value):
        if type(value) != bool:
            message = 'You should pass a boolean'
            raise TypeError(message)

        self._data['tokenize'] = value
