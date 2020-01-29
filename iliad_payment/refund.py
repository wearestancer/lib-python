# -*- coding: utf-8 -*-

from datetime import datetime

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call
from .config import Config
from .payment import Payment


class Refund(AbstractObject, AbstractAmount):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'

    _allowed_attributes = [
        'payment',
    ]

    def _init_date_bank(self, timestamp) -> datetime:
        return datetime.fromtimestamp(timestamp, tz=Config().default_timezone)

    @property
    def _init_payment(self) -> Payment:
        return Payment

    @property
    @populate_on_call
    def date_bank(self):
        """
        Value date.

        Returns:
            datetime: Value date of the refund.
        """
        return self._data.get('date_bank')

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
    def status(self) -> str:
        """
        Refund status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')
