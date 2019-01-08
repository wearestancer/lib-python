# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from .core.object import Object

_DEFAULT_MESSAGE = '{} must be have at between {} and {} characters'


class Customer(Object):
    """Representation of a customer."""

    @property
    def email(self):
        """
        Customer's email.

        Must be a string between 5 and 64 characters.
        """
        return self._data.get('email', None)

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError('Email must be a string')

        if len(value) < 5 or len(value) > 64:
            raise TypeError(_DEFAULT_MESSAGE.format('Email', 5, 64))

        self._data['email'] = value

    @property
    def mobile(self):
        """
        Customer's mobile phone number.

        Must be a string between 8 and 16 characters.
        """
        return self._data.get('mobile', None)

    @mobile.setter
    def mobile(self, value):
        if not isinstance(value, str):
            raise TypeError('Mobile phone must be a string')

        if len(value) < 8 or len(value) > 16:
            raise TypeError(_DEFAULT_MESSAGE.format('Mobile phone', 8, 16))

        self._data['mobile'] = value

    @property
    def name(self):
        """
        Customer's name.

        Must be a string between 4 and 64 characters.
        """
        return self._data.get('name', None)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Name must be a string')

        if len(value) < 4 or len(value) > 64:
            raise TypeError(_DEFAULT_MESSAGE.format('Name', 4, 64))

        self._data['name'] = value
