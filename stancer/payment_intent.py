# -*- coding: utf-8 -*-

import datetime
import re
from typing import Generator
from typing import TypeVar
from typing import Type
from typing import Any
from stancer.exceptions.invalid_value import InvalidSearchFilter
from .core.enum import Version
from .core.payment import PaymentCard
from .core.payment import PaymentCustomer

from .core.request import Request

from .card import Card
from .customer import Customer
from .payment import Payment
from .sepa import Sepa
from .core import AbstractAmount
from .core import AbstractObject
from .core import AbstractSearchInner
from .core import InnerSearchObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .core.helpers import coerce_methods_allowed
from .core.helpers import coerce_status
from .exceptions import InvalidAmountError, MissingPaymentMethodError
from .exceptions import InvalidPaymentIntentCaptureError
from .exceptions import InvalidPaymentIntentDescriptionError
from .exceptions import InvalidPaymentIntentOrderIdError
from .exceptions import InvalidPaymentIntentMethodsAllowed
from .exceptions import InvalidSepaError
from .exceptions import InvalidThreedsStatusError
from .exceptions import InvalidUrlError
from .exceptions import StancerNotImplementedError
from .exceptions import MissingPaymentIdError

CurrentInstance = TypeVar('CurrentInstance', bound='PaymentIntent')

ORDER_ID_MAX_LEN = 36


class PaymentIntent(
    AbstractObject, AbstractAmount, AbstractSearchInner, PaymentCard, PaymentCustomer
):
    _ENDPOINT = 'payment_intents'

    _version = Version.API_V2

    _allowed_attributes = [
        'capture',
        'created_at',
        'description',
        'metadata',
        'methods_allowed',
        'order_id',
        'return_url',
        'sepa',
        'status',
        'threeds',
        'url',
    ]

    @property
    def _init_sepa(self) -> Type[Sepa]:
        return Sepa

    @property
    def _init_card(self) -> Type[Card]:
        return Card

    @property
    def _init_customer(self) -> Type[Customer]:
        return Customer

    @property
    @populate_on_call
    def capture(self) -> bool:
        """
        Does the payment need to be captured or not.

        Args:
            value (bool): True if the payment must be captured, False if it must be authorized first

        Returns:
            bool: If the Payment intent must be captured or not.
        """
        return self._data.get('capture')

    @capture.setter
    @validate_type(bool, throws=InvalidPaymentIntentCaptureError)
    def capture(self, value: bool):
        self._data['capture'] = value

    # @property
    # @populate_on_call
    # def card(self) -> Optional[Card]:
    #     """
    #     Source card for the payment intent.
    #
    #     Args:
    #         value (Card): A valid `Card` object.
    #
    #     Returns:
    #         Card: Card used for the payment intent.
    #
    #     Raises:
    #         InvalidCardError: When card is invalid.
    #     """
    #     if self._data.get("card") is None:
    #         return None
    #
    #     return Card(self._data.get("card"))
    #
    # @card.setter
    # @validate_type(Card, throws=InvalidCardError)
    # def card(self, value: Card):
    #     if value.is_not_complete:
    #         message = "You must provide a complete Card."
    #         raise InvalidCardError(message)
    #     self._data["card"] = value.id
    #
    # @property
    # @populate_on_call
    # def customer(self) -> Optional[Customer]:
    #     """
    #     Customer handling the payment.
    #
    #     Args:
    #         value (Customer): A valid `Customer` object.
    #
    #     Returns:
    #         Customer: Customer handling the payment.
    #
    #     Raises:
    #         InvalidCustomerError: When customer is invalid.
    #     """
    #     if self._data.get("customer") is None:
    #         return None
    #     return Customer(self._data.get("customer"))
    #
    # @customer.setter
    # @validate_type(Customer, throws=InvalidCustomerError)
    # def customer(self, value: Customer):
    #     if value.is_not_complete:
    #         message = "You must provide a complete Customer."
    #         raise InvalidCustomerError(message)
    #     self._data["customer"] = value

    @property
    @populate_on_call
    def created_at(self) -> datetime.datetime:
        return self._data.get('created_at')

    # We overwrite created.
    @property
    @populate_on_call
    def created(self) -> None:
        return None

    def delete(self):
        """
        Delete the current object.

        Raises:
            StancerNotImplementedError: In every case, payment intents can not be
                delete, refund it.
        """
        message = (
            'You are not allowed to delete a payment intent, '
            'you need to refund it instead.'
        )

        raise StancerNotImplementedError(message)

    @property
    @populate_on_call
    def description(self) -> str:
        """
        Open description for your uses

        Args:
            value (str): Must be between 3 and 64 characters long.

        Returns:
            str: Payment Intent description

        Raises:
            InvalidPaymentIntentDescriptionError: When the description is invalid.
        """
        return self._data.get('description')

    @description.setter
    @validate_type(str, min=3, max=64, throws=InvalidPaymentIntentDescriptionError)
    def description(self, value: str):
        self._data['description'] = value

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
            params['order_id'] = cls.validate_order_id_params(
                kwargs['order_id'], ORDER_ID_MAX_LEN, base_message
            )
        if 'order' in kwargs:
            params['order'] = cls.validate_order_params(kwargs['order'])

        if 'card' in kwargs:
            card = kwargs['card']
            if isinstance(card, Card) and card.id is not None:
                card = card.id
            if not (isinstance(card, str) and re.match('^card_[a-zA-Z0-9]{24}$', card)):
                raise InvalidSearchFilter('Card must be a card ID.')
            params['card'] = card

        if 'sepa' in kwargs:
            sepa = kwargs['sepa']
            if isinstance(sepa, Sepa) and sepa.id is not None:
                sepa = sepa.id
            if not (isinstance(sepa, str) and re.match('^sepa_[a-zA-Z0-9]{24}$', sepa)):
                raise InvalidSearchFilter('Sepa must be a sepa ID.')
            params['sepa'] = sepa

        if 'field' in kwargs:
            if not (
                isinstance(kwargs['field'], str)
                and (kwargs['field'] in ('created', 'due'))
            ):
                raise InvalidSearchFilter("Field must be 'created' or 'due'.")

            params['field'] = kwargs['field']

        return params

    def get_payment_list(self, **kwargs) -> Generator:
        """
        Get A generator on the list of payment linked to the payment intent.

        args:
            (opt) limit (int): The number of payment fetched per request.
            (opt) start (int): The index of the first payment fetch, (default: 0).
        returns:
            (Generator) : A Generator that iterates on the payments linked to the payment intent
        """

        if self.id is None:
            raise MissingPaymentIdError(
                'you need an Id to acess inner route <id>/payments'
            )

        payments = self.list_inner(
            searched_class=Payment,
            inner_search_object=InnerSearchObject(self, inner_route='payments'),
            **kwargs,
        )
        return payments

    @property
    @populate_on_call
    def metadata(self) -> Any:
        """
        Metadata for this payment intent.

        Args:
            value(any): Metadata

        Returns:
            any: The metadata for this payment intent.

        """
        return self._data.get('metadata')

    @metadata.setter
    def metadata(self, value: Any):
        self._data['metadata'] = value

    @property
    @populate_on_call
    def methods_allowed(self) -> list:
        """
        Methods allowed for this payment intent.

        Args:
            value (list[MethodAllowed]): A list of method allowed.

        Returns:
            list[MethodAllowed]: The methods allowed for this payment intent.

        Raises:
            InvalidPaymentIntentMethodAllowed: when the list of payment methods is invalid.
        """
        return self._data.get('methods_allowed')

    @methods_allowed.setter
    @validate_type(
        list, coerce=coerce_methods_allowed, throws=InvalidPaymentIntentMethodsAllowed
    )
    def methods_allowed(self, value: list):
        self._data['methods_allowed'] = value

    @property
    @populate_on_call
    def order_id(self) -> str:
        """
        External Order Id linked to the payment Intent (not unique).

        Args:
            value (string): An Order ID no longer than 36 character.

        Returns:
            string: The external order ID.

        Raises:
            InvalidPaymentIntentOrderId: when the order ID is invalid.
        """
        return self._data.get('order_id')

    @order_id.setter
    @validate_type(str, min=1, max=36, throws=InvalidPaymentIntentOrderIdError)
    def order_id(self, value: str):
        self._data['order_id'] = value

    @property
    @populate_on_call
    def return_url(self) -> str:
        """
        Return URL.

        Args:
            value: New URL, must an HTTPS URL.

        Returns:
            Location of the page you'll be redirected to, after 3DS authentication.

        Raises:
            InvalidUrlError: when the url is not valid (or not secure http).
        """
        return self._data.get('return_url')

    @return_url.setter
    @validate_type(
        str,
        validation=lambda v: (
            None if v.startswith('https://') else 'Must be an HTTPS URL'
        ),
        throws=InvalidUrlError,
    )
    def return_url(self, value: str):
        self._data['return_url'] = value

    def send(self: CurrentInstance) -> CurrentInstance:
        """
        Create or Update the payment.

        Returns:
            Current instance.

        Raises:
            InvalidAmountError: When Called without any amount setted.
            StancerHTTPError: On error during with the API (may be child instance
                of StancerHTTPError).
            MissingPaymentMethodError: When called without any payment method
                or if this method is uncomplete
                (you may have forgotten the card number).
        """
        if self.amount is None:
            message = 'You must provide an amount before sending a payment.'
            raise InvalidAmountError(message)

        if self.card is not None and self.card.is_not_complete:
            message = 'Your card is incomplete.'
            raise MissingPaymentMethodError(message)

        if self.sepa is not None and self.sepa.is_not_complete:
            message = 'Your SEPA account is incomplete.'
            raise MissingPaymentMethodError(message)

        return super().send()

    def send_capture(self: CurrentInstance) -> CurrentInstance:
        """
        A method to capture the payment intent manually.

        Returns:
            self: The Paiment Intent captured
        Raises:

        """
        if self.id is None:
            raise MissingPaymentIdError(
                'you need an Id to acess inner route <id>/capture'
            )

        Request().post(self, inner_route='/capture')
        return self

    @property
    @populate_on_call
    def sepa(self) -> Sepa:
        """
        Source SEPA account for the payment intent.

        Args:
            value (Sepa): A valid `Sepa` object.

        Returns:
            Sepa: SEPA used for the payment intent.

        Raises:
            InvalidSepaError: When sepa is invalid.
        """
        return self._data.get('sepa')

    @sepa.setter
    @validate_type(Sepa, throws=InvalidSepaError)
    def sepa(self, value: Sepa):
        self._data['sepa'] = value

    @property
    @populate_on_call
    def status(self) -> str:
        """
        The status of the payment intent

        Args:
            value (PaymentIntentStatus) : A valid Status.

        Returns:
            PaymentIntentStatus: Status of the payment intent

        Raises:
            InvalidPaymentIntentStatus: When the payment intent status is invalid.
        """
        return self._data.get('status')

    @property
    @populate_on_call
    def threeds(self) -> str:
        """
        The status of the 3ds either 'required' if required or 'none' if not
        Threeds status is not auth status !

        Arg:
            value (ThreedsStatus): The threeds status.

        Returns:
            ThreedsStatus : The status of the threeds .

        """
        return self._data.get('threeds')

    @threeds.setter
    @validate_type(str, coerce=coerce_status, throws=InvalidThreedsStatusError)
    def threeds(self, value: str):
        self._data['threeds'] = value

    @property
    @populate_on_call
    def url(self) -> str:
        """
        The payment Page Url, to pay the Payment Intent

        Returns:
            Url: The url of the payment page
        """
        return self._data.get('url')
