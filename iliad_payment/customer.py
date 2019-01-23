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

from .core import AbstractCountry
from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidCustomerEmailError
from .exceptions import InvalidCustomerMobileError


class Customer(AbstractObject, AbstractName, AbstractCountry):
    """Representation of a customer."""

    _ENDPOINT = 'customers'

    _allowed_attributes = [
        'email',
        'mobile',
    ]

    @property
    @populate_on_call
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
    @validate_type(str, min=5, max=64, throws=InvalidCustomerEmailError)
    def email(self, value):
        self._data['email'] = value

    @property
    def is_complete(self):
        """
        Indicate if all mandatory customer data are provided.

        Returns:
            bool: Is the customer complete ?
        """
        if self.email is None and self.mobile is None:
            return False

        return True

    @property
    def is_not_complete(self):
        """
        Indicate if all mandatory customer data are NOT provided.

        It's simply a `not self.is_complete`.

        Returns:
            bool: Is the customer not complete ?
        """
        return not self.is_complete

    @property
    @populate_on_call
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
    @validate_type(
        str,
        min=8,
        max=16,
        name='Mobile phone',
        throws=InvalidCustomerMobileError,
    )
    def mobile(self, value):
        self._data['mobile'] = value
