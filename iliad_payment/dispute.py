# -*- coding: utf-8 -*-

from .core import AbstractAmount
from .core import AbstractObject
from .core import AbstractSearch
from .core.decorators import populate_on_call
from .payment import Payment


class Dispute(AbstractObject, AbstractAmount, AbstractSearch):
    """Representation of a dispute."""

    _ENDPOINT = 'disputes'

    @property
    def _init_payment(self) -> Payment:
        return Payment

    @property
    @populate_on_call
    def order_id(self) -> str:
        """
        External order id.

        Returns:
            str: External order ID.
        """
        return self._data.get('order_id')

    @property
    @populate_on_call
    def payment(self) -> Payment:
        """
        Original payment.

        Returns:
            Payment: Original payment.
        """
        return self._data.get('payment')

    @property
    @populate_on_call
    def response(self) -> str:
        """
        API response code.

        Returns:
            str: API response for the dispute.
        """
        return self._data.get('response')
