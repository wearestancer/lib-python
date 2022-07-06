# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TypeVar

from .card import Card
from .customer import Customer
from .sepa import Sepa
from .core import AbstractAmount
from .core import AbstractCountry
from .core import AbstractObject
from .core import AbstractSearch
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .core.helpers import coerce_status
from .core.helpers import coerce_uuid
from .core.payment.auth import PaymentAuth
from .core.payment.page import PaymentPage
from .core.payment.refund import PaymentRefund
from .exceptions import StancerNotImplementedError
from .exceptions import InvalidAmountError
from .exceptions import InvalidCardError
from .exceptions import InvalidCurrencyError
from .exceptions import InvalidCustomerError
from .exceptions import InvalidPaymentCaptureError
from .exceptions import InvalidPaymentDescriptionError
from .exceptions import InvalidPaymentOrderIdError
from .exceptions import InvalidPaymentUniqueIdError
from .exceptions import InvalidSearchFilter
from .exceptions import InvalidSepaError
from .exceptions import InvalidStatusError
from .exceptions import MissingPaymentMethodError
from .status.payment import PaymentStatus


BaseObject = (
    AbstractObject,
    AbstractAmount,
    AbstractCountry,
    AbstractSearch,
    PaymentAuth,
    PaymentPage,
    PaymentRefund,
)
CurrentInstance = TypeVar('CurrentInstance', bound='Payment')

ORDER_ID_MAX_LEN = 36
UNIQUE_ID_MAX_LEN = 36


class Payment(*BaseObject):
    """Representation of a payment."""

    _ENDPOINT = 'checkout'  # pylint: disable=invalid-name

    _allowed_attributes = [
        'capture',
        'card',
        'customer',
        'description',
        'order_id',
        'sepa',
        'status',
        'unique_id',
    ]
    _datetime_property = [
        'date_bank',
    ]

    @property
    def _init_card(self) -> Card:
        return Card

    @property
    def _init_customer(self) -> Customer:
        return Customer

    @property
    def _init_sepa(self) -> Sepa:
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
    def capture(self, value: bool):
        self._data['capture'] = value

    @property
    @populate_on_call
    def card(self) -> Card:
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
    def card(self, value: Card):
        self._data['card'] = value
        self._data['method'] = 'card'

    @property
    @populate_on_call
    def customer(self) -> Customer:
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
    def customer(self, value: Customer):
        self._data['customer'] = value

    @property
    @populate_on_call
    def date_bank(self) -> datetime:
        """
        Value date.

        Returns:
            Payment value date.
        """
        return self._data.get('date_bank')

    def delete(self):
        """
        Delete the current object.

        Raises:
            StancerNotImplementedError: In every case, payments can not be
                delete, refund it.
        """
        message = (
            'You are not allowed to delete a payment, '
            'you need to refund it instead.'
        )

        raise StancerNotImplementedError(message)

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
    def fee(self) -> datetime:
        """
        Fee applied at checkout.

        Returns:
            Fee applied at checkout.
        """
        return self._data.get('fee')

    @classmethod
    def filter_list_params(cls, **kwargs) -> dict:
        """
        Filter for list method.

        Allow `order_id` and `unique_id` parameters.

        Args:
            kwargs: Arbitrary keyword argument to filter.

        Returns:
            Filtered arguments.
        """

        params = {}
        base_message = 'A valid {} must be between {} and {} characters.'

        if 'order_id' in kwargs:
            if not isinstance(kwargs['order_id'], str):
                raise InvalidSearchFilter('Order ID must be a string.')

            length = len(kwargs['order_id'])

            if length > ORDER_ID_MAX_LEN or length == 0:
                raise InvalidSearchFilter(base_message.format('order ID', 1, ORDER_ID_MAX_LEN))

            params['order_id'] = kwargs['order_id']

        if 'unique_id' in kwargs:
            if not isinstance(kwargs['unique_id'], str):
                raise InvalidSearchFilter('Unique ID must be a string.')

            length = len(kwargs['unique_id'])

            if length > UNIQUE_ID_MAX_LEN or length == 0:
                raise InvalidSearchFilter(base_message.format('unique ID', 1, UNIQUE_ID_MAX_LEN))

            params['unique_id'] = kwargs['unique_id']

        return params

    @property
    def is_error(self) -> bool:
        """
        Is the operation an error ?

        Returns:
            Is the operation an error ?
        """
        if self.status is None:
            return False

        return not self.is_success

    @property
    @populate_on_call
    def is_not_error(self) -> bool:
        """
        Is the operation not an error ?

        Basicaly, it's just a `not self.is_error`.

        Returns:
            Is the operation not an error ?
        """
        return not self.is_error

    @property
    @populate_on_call
    def is_not_success(self) -> bool:
        """
        Is the operation not a success ?

        Basicaly, it's just a `not self.is_success`.

        Returns:
            Is the operation not a success ?
        """
        return not self.is_success

    @property
    @populate_on_call
    def is_success(self) -> bool:
        """
        Is the operation a success ?

        Returns:
            Is the operation a success ?
        """
        if self.status is None:
            return False

        if self.status == PaymentStatus.AUTHORIZED:
            return not self.capture

        return self.status in (PaymentStatus.CAPTURED, PaymentStatus.TO_CAPTURE)

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
            value (str): Must be maximum 36 characters.

        Returns:
            str: External order ID.

        Raises:
            InvalidPaymentOrderIdError: When order id is invalid.
        """
        return self._data.get('order_id')

    @order_id.setter
    @validate_type(
        str,
        coerce=coerce_uuid,
        max=ORDER_ID_MAX_LEN,
        name='Order id',
        throws=InvalidPaymentOrderIdError,
    )
    def order_id(self, value: str):
        self._data['order_id'] = value

    @property
    @populate_on_call
    def response(self) -> str:
        """
        API response code.

        `00` is a success, other codes are errors.
        You may use `Payment.response_message` to get the reason.

        Returns:
            str: API response for the payment.
        """
        return self._data.get('response')

    @property
    @populate_on_call
    def response_message(self) -> str:
        """
        API response message.

        See `Payment.response`.

        Returns:
            str: API response message.
        """
        response = self.response
        responses = {
            '00': 'OK',
            '05': 'Do not honor',
            '41': 'Lost card',
            '42': 'Stolen card',
            '51': 'Insufficient funds',
        }

        return responses.get(response)

    def send(self) -> CurrentInstance:
        """
        Create or update the payment.

        Returns:
            Current instance.

        Raises:
            InvalidAmountError: When called without any amount setted.
            InvalidCurrencyError: When called without any currency.
            StancerHTTPError: On error during with the API (may be child instance
                of StancerHTTPError).
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

        if self.card is not None and self.card.is_not_complete:
            message = 'Your card is incomplete.'
            raise MissingPaymentMethodError(message)

        if self.sepa is not None and self.sepa.is_not_complete:
            message = 'Your SEPA account is incomplete.'
            raise MissingPaymentMethodError(message)

        self._create_device()

        return super().send()

    @property
    @populate_on_call
    def sepa(self) -> Sepa:
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
    def sepa(self, value: Sepa):
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

    @status.setter
    @validate_type(str, coerce=coerce_status, throws=InvalidStatusError)
    def status(self, value: str):
        self._data['status'] = value

    @property
    @populate_on_call
    def unique_id(self) -> str:
        """
        External unique ID.

        If a `unique_id` is provided, it will used to deduplicate payments.

        This should be used only with an identifier unique in your system.
        You should use an auto-increment or a UUID made in your environment.

        Args:
            value (str): Must be maximum 36 characters.

        Returns:
            str: External unique ID.

        Raises:
            InvalidPaymentUniqueIdError: When unique id is invalid.
        """
        return self._data.get('unique_id')

    @unique_id.setter
    @validate_type(
        str,
        coerce=coerce_uuid,
        max=UNIQUE_ID_MAX_LEN,
        name='Unique ID',
        throws=InvalidPaymentUniqueIdError,
    )
    def unique_id(self, value: str):
        self._data['unique_id'] = value
