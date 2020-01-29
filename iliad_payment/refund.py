# -*- coding: utf-8 -*-

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call
from .payment import Payment


class Refund(AbstractObject, AbstractAmount):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'

    _allowed_attributes = [
        'payment',
    ]

    @property
    def _init_payment(self) -> Payment:
        return Payment

    @property
    @populate_on_call
    def payment(self) -> Payment:
        """
        Original payment.

        Returns:
            Payment: Original payment.
        """
        return self._data.get('payment')
