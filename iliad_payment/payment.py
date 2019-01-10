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

from .card import Card
from .customer import Customer
from .sepa import Sepa
from .core import AbstractObject, AbstractAmount


class Payment(AbstractObject, AbstractAmount):
    """Representation of a payment."""

    @property
    def capture(self):
        """Do we need to capture the payment ?"""
        return self._data.get('capture', None)

    @capture.setter
    def capture(self, value):
        if not isinstance(value, bool):
            raise TypeError('Capture must be a boolean')

        self._data['capture'] = value

    @property
    def card(self):
        """Target card for the payment."""
        return self._data.get('card', None)

    @card.setter
    def card(self, value):
        if not isinstance(value, Card):
            raise TypeError('You must provide a valid instance of Card')

        self._data['card'] = value
        self._data['method'] = 'card'

    @property
    def customer(self):
        """Customer handling the payment."""
        return self._data.get('customer', None)

    @customer.setter
    def customer(self, value):
        if not isinstance(value, Customer):
            raise TypeError('You must provide a valid instance of Customer')

        self._data['customer'] = value

    @property
    def description(self):
        """Open description for your uses."""
        return self._data.get('description', None)

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError('Description must be a string')

        (length_min, length_max) = (3, 64)

        if len(value) < length_min or len(value) > length_max:
            tmp = 'A valid description must be between {} and {} characters'

            raise TypeError(tmp.format(length_min, length_max))

        self._data['description'] = value

    @property
    def method(self):
        """Payment method used."""
        return self._data.get('method', None)

    @property
    def order_id(self):
        """External order id."""
        return self._data.get('order_id', None)

    @order_id.setter
    def order_id(self, value):
        if not isinstance(value, str):
            raise TypeError('Order id must be a string')

        length_max = 24

        if len(value) > length_max:
            tmp = 'Order id must have maximum {} characters'

            raise TypeError(tmp.format(length_max))

        self._data['order_id'] = value

    @property
    def response_code(self):
        """API response code."""
        return self._data.get('response_code', None)

    @property
    def response_message(self):
        """API response message."""
        response_code = self.response_code
        responses = {
            '00': 'OK',
            '05': 'Do not honor',
            '41': 'Lost card',
            '42': 'Stolen card',
            '51': 'Insufficient funds',
        }

        return responses.get(response_code, None)

    @property
    def sepa(self):
        """Target sepa account for the payment."""
        return self._data.get('sepa', None)

    @sepa.setter
    def sepa(self, value):
        if not isinstance(value, Sepa):
            raise TypeError('You must provide a valid instance of Sepa')

        self._data['sepa'] = value
        self._data['method'] = 'sepa'

    @property
    def status(self):
        """Payment status."""
        return self._data.get('status', None)
