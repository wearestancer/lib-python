# -*- coding: utf-8 -*-

import re

from typing import Any
from typing import Callable
from typing import Generator
from typing import Type
from typing import TypeVar

from stancer.exceptions.invalid_value import InvalidSearchFilter
from stancer.status.method_allowed import MethodAllowed

from .card import Card
from .core.abstract_amount import AbstractAmount
from .core.abstract_object import AbstractObject
from .core.abstract_search_inner import AbstractSearchInner
from .core.decorators.populate_on_call import populate_on_call
from .core.decorators.validate_type import validate_type
from .core.enum.version import Version
from .core.helpers.coerce_status import coerce_status
from .core.inner_search_object import InnerSearchObject
from .core.payment.card import PaymentCard
from .core.payment.customer import PaymentCustomer
from .core.payment.sepa import PaymentSepa
from .core.request import Request
from .customer import Customer
from .exceptions import InvalidAmountError
from .exceptions import InvalidPaymentIntentCaptureError
from .exceptions import InvalidPaymentIntentDescriptionError
from .exceptions import InvalidPaymentIntentMethodsAllowed
from .exceptions import InvalidPaymentIntentOrderIdError
from .exceptions import InvalidThreedsStatusError
from .exceptions import InvalidUrlError
from .exceptions import MissingPaymentIdError
from .exceptions import MissingPaymentMethodError
from .exceptions import StancerNotImplementedError
from .payment import Payment
from .sepa import Sepa

try:
    from typing import Never  # type: ignore
except ImportError:
    from typing import NoReturn as Never
CurrentInstance = TypeVar('CurrentInstance', bound='PaymentIntent')

ORDER_ID_MAX_LEN = 36


def coerce_methods_allowed(
    value: list[str | MethodAllowed] | str | MethodAllowed | None,
) -> list[str | None]:
    """
    Transform a list of enum instance into a list string.

    Args:
        value: Value to coerce.

    Returns:
        Transformed string list if value was an enum, otherwise the list directly.
    """
    if not value or value is None:
        raise InvalidPaymentIntentMethodsAllowed()

    # Coerce is called before type validation.
    # If we don't check the type first we can have a type error when we try to iterate
    if not isinstance(value, list):
        value = [value]

    if not value or len(
        list(
            filter(
                lambda tested_value: isinstance(tested_value, MethodAllowed)
                or MethodAllowed.has_value(str(tested_value)),
                value,
            )
        )
    ) != len(value):
        raise InvalidPaymentIntentMethodsAllowed()

    return list(map(coerce_status, value))


class PaymentIntent(
    AbstractObject,
    AbstractAmount,
    AbstractSearchInner,
    PaymentCard,
    PaymentCustomer,
    PaymentSepa,
):  # pylint: disable='too-many-ancestors'
    # our way of building object imposes many ancestors
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
    def capture(self) -> bool | None:
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
    def capture(self, value: bool) -> None:
        self._data['capture'] = value

    def delete(self) -> Never:
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
    def description(self) -> str | None:
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
    def description(self, value: str) -> None:
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

    def get_payment_list(self, **kwargs) -> Callable[[], Generator]:
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
    def methods_allowed(self) -> list | None:
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
    def methods_allowed(self, value: list) -> None:
        self._data['methods_allowed'] = value

    @property
    @populate_on_call
    def order_id(self) -> str | None:
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
    def order_id(self, value: str) -> None:
        self._data['order_id'] = value

    @property
    @populate_on_call
    def return_url(self) -> str | None:
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
    def return_url(self, value: str) -> None:
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
    def status(self) -> str | None:
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
    def threeds(self) -> str | None:
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
    def url(self) -> str | None:
        """
        The payment Page Url, to pay the Payment Intent

        Returns:
            Url: The url of the payment page
        """
        return self._data.get('url')
