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
