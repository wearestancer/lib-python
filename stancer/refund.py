# -*- coding: utf-8 -*-


from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call

if TYPE_CHECKING:
    from .payment import Payment


class Refund(AbstractObject, AbstractAmount):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'

    _allowed_attributes = [
        'payment',
    ]
    _datetime_property = [
        'date_bank',
        'date_refund',
    ]

    def __init__(self, uid: str | None = None, **kwargs):
        """
        Create or get a Refund object.

        You can optionaly pass an id uppon instanciation, it will be used to
        get current object data on the API.

        If you did not provide an id, the current object will be a new API
        object.

        You may also pass keywords arguments, we will use them hydrate the object.

        Args:
            uid: Object identifier.
            **kwargs: Arbitrary keyword arguments, used to hydrate the object.

        Returns:
            An instance of the current object.
        """
        super().__init__(uid, **kwargs)
        self._modified = 'payment'

    @property
    def _init_payment(self) -> type['Payment']:
        from .payment import Payment  # pylint: disable=import-outside-toplevel

        return Payment

    @property
    @populate_on_call
    def date_bank(self) -> datetime | None:
        """
        Value date.

        Returns:
            datetime: Value date of the refund.
        """
        return self._data.get('date_bank')

    @property
    @populate_on_call
    def date_refund(self) -> datetime | None:
        """
        Date when the refund is sent to the bank.

        Returns:
            datetime: When refund was sent to the bank.
        """
        return self._data.get('date_refund')

    @property
    @populate_on_call
    def payment(self) -> 'Payment | None':
        """
        Original payment.

        Returns:
            Payment: Original payment.
        """
        return self._data.get('payment')

    @property
    @populate_on_call
    def status(self) -> str | None:
        """
        Refund status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')

    def to_json_repr(self) -> dict[str, Any] | str:
        """
        Return a dictionnary which will be used to make a JSON representation.

        Returns:
            A JSON still as a dictionnary.
        """
        representation = super().to_json_repr()

        if isinstance(self.payment, AbstractObject) and not isinstance(
            representation, str
        ):
            representation['payment'] = self.payment.id

        return representation
