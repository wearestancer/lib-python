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

from .core.abstract_name import AbstractName
from .core.abstract_object import AbstractObject

_DEFAULT_MESSAGE = '{} must be have at between {} and {} characters'


class Customer(AbstractObject, AbstractName):
    """Representation of a customer."""

    _ENDPOINT = 'customers'

    @property
    def email(self):
        """
        Customer's email.

        Args:
            value (str): New email, must be between 5 and 64 characters.

        Returns:
            str: Customer's email.
        """
        return self._data.get('email')

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError('Email must be a string')

        if len(value) < 5 or len(value) > 64:
            raise TypeError(_DEFAULT_MESSAGE.format('Email', 5, 64))

        self._data['email'] = value
        self._modified = True

    @property
    def mobile(self):
        """
        Customer's mobile phone number.

        Args:
            value (str): New mobile, must be between 8 and 16 characters.

        Returns:
            str: Customer's mobile phone number.
        """
        return self._data.get('mobile')

    @mobile.setter
    def mobile(self, value):
        if not isinstance(value, str):
            raise TypeError('Mobile phone must be a string')

        if len(value) < 8 or len(value) > 16:
            raise TypeError(_DEFAULT_MESSAGE.format('Mobile phone', 8, 16))

        self._data['mobile'] = value
        self._modified = True
