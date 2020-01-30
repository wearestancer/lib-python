# -*- coding: utf-8 -*-

from typing import TypeVar

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


CurrentInstance = TypeVar('CurrentInstance', bound='Payment')

CardInstance = TypeVar('CurrentInstance', bound='Card')
CustomerInstance = TypeVar('CurrentInstance', bound='Customer')
SepaInstance = TypeVar('CurrentInstance', bound='Sepa')


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
    def _init_card(self) -> CardInstance:
        return Card

    @property
    def _init_customer(self) -> CustomerInstance:
        return Customer

    @property
    def _init_sepa(self) -> SepaInstance:
        return Sepa

    @property
    @populate_on_call
    def capture(self) -> bool:
        """
        Do we need to capture the payment ?

        When `False` the payment acts as an authorization and need to be
        capture later.

        Args:
            value: New status for capture.

        Returns:
            Current capture status.

        Raises:
            InvalidPaymentCaptureError: When capture flag is invalid.
        """
        return self._data.get('capture')

    @capture.setter
    @validate_type(bool, throws=InvalidPaymentCaptureError)
    def capture(self, value) -> str:
        self._data['capture'] = value

    @property
    @populate_on_call
    def card(self) -> CardInstance:
        """
        Source card for the payment.

        Args:
            value (Card): A valid `Card` object.

        Returns:
            Card: Card used for the payment.

        Raises:
            InvalidCardError: When card is invalid.
        """
        return self._data.get('card')

    @card.setter
    @validate_type(Card, throws=InvalidCardError)
    def card(self, value: CardInstance):
        self._data['card'] = value
        self._data['method'] = 'card'

    @property
    @populate_on_call
    def customer(self) -> CustomerInstance:
        """
        Customer handling the payment.

        Args:
            value (Customer): A valid `Customer` object.

        Returns:
            Customer: Customer handling the payment.

        Raises:
            InvalidCustomerError: When customer is invalid.
        """
        return self._data.get('customer')

    @customer.setter
    @validate_type(Customer, throws=InvalidCustomerError)
    def customer(self, value: CustomerInstance):
        self._data['customer'] = value

    def delete(self):
        """
        Delete the current object.

        Raises:
            IliadNotImplementedError: In every case, payments can not be
                delete, refund it.
        """
        message = (
            'You are not allowed to delete a payment, '
            'you need to refund it instead.'
        )

        raise IliadNotImplementedError(message)

    @property
    @populate_on_call
    def description(self) -> str:
        """
        Open description for your uses.

        Args:
            value (str): Must be between 3 and 64 characters.

        Returns:
            str: Payment description.

        Raises:
            InvalidPaymentDescriptionError: When description is invalid.
        """
        return self._data.get('description')

    @description.setter
    @validate_type(str, min=3, max=64, throws=InvalidPaymentDescriptionError)
    def description(self, value: str):
        self._data['description'] = value

    @property
    @populate_on_call
    def is_success(self) -> bool:
        """
        Is the operation a success ?

        Returns:
            Is the operation a success ?
        """
        return self.response_code == '00'

    @property
    def is_error(self) -> bool:
        """
        Is the operation an error ?

        Returns:
            Is the operation an error ?
        """
        return not self.is_success

    @property
    @populate_on_call
    def live_mode(self) -> bool:
        """
        Indicate if we are in live or test mode.

        True => live / False => test

        Returns:
            Are we in live mode ?
        """
        return self._data.get('live_mode')

    @property
    @populate_on_call
    def method(self) -> str:
        """
        Payment method used.

        Returns:
            str: Payment means used, should be "card" or "sepa".
        """
        return self._data.get('method')

    @property
    @populate_on_call
    def order_id(self) -> str:
        """
        External order id.

        Like `Payment.description`, this is not used by the API,
        it allow you to add your ID to a payment.

        Args:
            value (str): Must be maximum 24 characters.

        Returns:
            str: External order ID.

        Raises:
            InvalidPaymentOrderIdError: When order id is invalid.
        """
        return self._data.get('order_id')

    @order_id.setter
    @validate_type(
        str,
        max=24,
        name='Order id',
        throws=InvalidPaymentOrderIdError,
    )
    def order_id(self, value: str):
        self._data['order_id'] = value

    @property
    @populate_on_call
    def response_code(self) -> str:
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
    def response_message(self) -> str:
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

    def save(self) -> CurrentInstance:
        """
        Create or update the payment.

        Returns:
            Current instance.

        Raises:
            InvalidAmountError: When called without any amount setted.
            InvalidCurrencyError: When called without any currency.
            IliadHTTPError: On error during with the API (may be child instance of IliadHTTPError).
            MissingPaymentMethodError: When called without any payment method
                or if this method is uncomplete
                (you may have forgotten the card number).
        """
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

        return super(Payment, self).save()

    @property
    @populate_on_call
    def sepa(self) -> SepaInstance:
        """
        Source SEPA account for the payment.

        Args:
            value (Sepa): A valid `Sepa` object.

        Returns:
            Sepa: SEPA used for the payment.

        Raises:
            InvalidSepaError: When sepa is invalid.
        """
        return self._data.get('sepa')

    @sepa.setter
    @validate_type(Sepa, throws=InvalidSepaError)
    def sepa(self, value: str):
        self._data['sepa'] = value
        self._data['method'] = 'sepa'

    @property
    @populate_on_call
    def status(self) -> str:
        """
        Payment status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')
