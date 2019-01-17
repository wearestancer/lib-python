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
from .core.decorators import populate_on_call


class Payment(AbstractObject, AbstractAmount):
    """Representation of a payment."""

    _ENDPOINT = 'checkout'

    _filtered_attributes = [
        'method',
    ]

    @property
    @populate_on_call
    def capture(self):
        """
        Do we need to capture the payment ?

        When `False` the payment acts as an authorization and need to be
        capture later.

        Args:
            value (bool): New status for capture.

        Returns:
            bool: Current capture status.
        """
        return self._data.get('capture')

    @capture.setter
    def capture(self, value):
        if not isinstance(value, bool):
            raise TypeError('Capture must be a boolean')

        self._data['capture'] = value
        self._modified = True

    @property
    def card(self):
        """
        Source card for the payment.

        Args:
            value (Card): A valid `Card` object.

        Returns:
            Card: Card used for the payment.
        """
        return self._data.get('card')

    @card.setter
    def card(self, value):
        if not isinstance(value, Card):
            raise TypeError('You must provide a valid instance of Card')

        self._data['card'] = value
        self._data['method'] = 'card'
        self._modified = True

    @property
    def customer(self):
        """
        Customer handling the payment.

        Args:
            value (Customer): A valid `Customer` object.

        Returns:
            Customer: Customer handling the payment.
        """
        return self._data.get('customer')

    @customer.setter
    def customer(self, value):
        if not isinstance(value, Customer):
            raise TypeError('You must provide a valid instance of Customer')

        self._data['customer'] = value
        self._modified = True

    @property
    @populate_on_call
    def description(self):
        """
        Open description for your uses.

        Args:
            value (str): Must be between 3 and 64 characters.

        Returns:
            str: Payment description.
        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError('Description must be a string')

        (length_min, length_max) = (3, 64)

        if len(value) < length_min or len(value) > length_max:
            tmp = 'A valid description must be between {} and {} characters'

            raise TypeError(tmp.format(length_min, length_max))

        self._data['description'] = value
        self._modified = True

    @property
    @populate_on_call
    def method(self):
        """
        Payment method used.

        Returns:
            str: Payment means used, should be "card" or "sepa".
        """
        return self._data.get('method')

    @property
    @populate_on_call
    def order_id(self):
        """
        External order id.

        Like `Payment.description`, this is not used by the API,
        it allow you to add your ID to a payment.

        Args:
            value (str): Must be maximum 24 characters.

        Returns:
            str: External order ID.
        """
        return self._data.get('order_id')

    @order_id.setter
    def order_id(self, value):
        if not isinstance(value, str):
            raise TypeError('Order id must be a string')

        length_max = 24

        if len(value) > length_max:
            tmp = 'Order id must have maximum {} characters'

            raise TypeError(tmp.format(length_max))

        self._data['order_id'] = value
        self._modified = True

    @property
    @populate_on_call
    def response_code(self):
        """
        API response code.

        `00` is a success, other codes are errors.
        You may use `Payment.response_message` to get the reason.

        Returns:
            str: API response for the payment.
        """
        return self._data.get('response_code')

    @property
    @populate_on_call
    def response_message(self):
        """
        API response message.

        See `Payment.response_code`.

        Returns:
            str: API response message.
        """
        response_code = self.response_code
        responses = {
            '00': 'OK',
            '05': 'Do not honor',
            '41': 'Lost card',
            '42': 'Stolen card',
            '51': 'Insufficient funds',
        }

        return responses.get(response_code)

    @property
    def sepa(self):
        """
        Source SEPA account for the payment.

        Args:
            value (Sepa): A valid `Sepa` object.

        Returns:
            Sepa: SEPA used for the payment.
        """
        return self._data.get('sepa')

    @sepa.setter
    def sepa(self, value):
        if not isinstance(value, Sepa):
            raise TypeError('You must provide a valid instance of Sepa')

        self._data['sepa'] = value
        self._data['method'] = 'sepa'
        self._modified = True

    @property
    @populate_on_call
    def status(self):
        """
        Payment status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')
