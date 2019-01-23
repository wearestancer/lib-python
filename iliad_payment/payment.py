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
from .core import AbstractAmount
from .core import AbstractCountry
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import IliadNotImplementedError
from .exceptions import InvalidAmountError
from .exceptions import InvalidCardError
from .exceptions import InvalidCurrencyError
from .exceptions import InvalidCustomerError
from .exceptions import InvalidPaymentCaptureError
from .exceptions import InvalidPaymentDescriptionError
from .exceptions import InvalidPaymentOrderIdError
from .exceptions import InvalidSepaError
from .exceptions import MissingPaymentMethodError


class Payment(AbstractObject, AbstractAmount, AbstractCountry):
    """Representation of a payment."""

    _ENDPOINT = 'checkout'

    _allowed_attributes = [
        'capture',
        'card',
        'customer',
        'description',
        'order_id',
        'sepa',
    ]

    @property
    def _init_card(self):
        self.card = Card()

        return self.card

    @property
    def _init_customer(self):
        self.customer = Customer()

        return self.customer

    @property
    def _init_sepa(self):
        self.sepa = Sepa()

        return self.sepa

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
    @validate_type(bool, throws=InvalidPaymentCaptureError)
    def capture(self, value):
        self._data['capture'] = value

    @property
    @populate_on_call
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
    @validate_type(Card, throws=InvalidCardError)
    def card(self, value):
        self._data['card'] = value
        self._data['method'] = 'card'

    @property
    @populate_on_call
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
    @validate_type(Customer, throws=InvalidCustomerError)
    def customer(self, value):
        self._data['customer'] = value

    def delete(self):
        message = (
            'You are not allowed to delete a payment, '
            'you need to refund it instead.'
        )

        raise IliadNotImplementedError(message)

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
    @validate_type(str, min=3, max=64, throws=InvalidPaymentDescriptionError)
    def description(self, value):
        self._data['description'] = value

    @property
    @populate_on_call
    def is_success(self):
        """
        Is the operation a success ?

        Returns:
            bool: Is the operation a success ?
        """
        return self.response_code == '00'

    @property
    def is_error(self):
        """
        Is the operation an error ?

        Returns:
            bool: Is the operation an error ?
        """
        return not self.is_success

    @property
    @populate_on_call
    def live_mode(self):
        """
        Indicate if we are in live or test mode.

        True => live / False => test

        Returns:
            bool: Are we in live mode ?
        """
        return self._data.get('live_mode')

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
    @validate_type(
        str,
        max=24,
        name='Order id',
        throws=InvalidPaymentOrderIdError,
    )
    def order_id(self, value):
        self._data['order_id'] = value

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

    def save(self):
        if self.amount is None:
            message = 'You must provide an amount before sending a payment.'
            raise InvalidAmountError(message)

        if self.currency is None:
            message = 'You must provide a currency before sending a payment.'
            raise InvalidCurrencyError(message)

        message = (
            'You must provide a valid credit card '
            'or SEPA account before sending a payment.'
        )

        if self.card is None and self.sepa is None:
            raise MissingPaymentMethodError(message)

        if self.card is not None and self.card.is_not_complete:
            message += ' Your card is incomplete.'
            raise MissingPaymentMethodError(message)

        if self.sepa is not None and self.sepa.is_not_complete:
            message += ' Your SEPA account is incomplete.'
            raise MissingPaymentMethodError(message)

        return super().save()

    @property
    @populate_on_call
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
    @validate_type(Sepa, throws=InvalidSepaError)
    def sepa(self, value):
        self._data['sepa'] = value
        self._data['method'] = 'sepa'

    @property
    @populate_on_call
    def status(self):
        """
        Payment status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')
