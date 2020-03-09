# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TypeVar

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call
from .config import Config
from .payment import Payment

CurrentInstance = TypeVar('CurrentInstance', bound='Refund')


class Refund(AbstractObject, AbstractAmount):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'

    _allowed_attributes = [
        'payment',
    ]

    def _init_date_bank(self, timestamp) -> datetime:  # pylint: disable=no-self-use
        return datetime.fromtimestamp(timestamp, tz=Config().default_timezone)

    def _init_date_refund(self, timestamp) -> datetime:  # pylint: disable=no-self-use
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
    def date_refund(self):
        """
        Date when the refund is sent to the bank.

        Returns:
            datetime: When refund was sent to the bank.
        """
        return self._data.get('date_refund')

    @property
    @populate_on_call
    def payment(self) -> Payment:
        """
        Original payment.

        Returns:
            Payment: Original payment.
        """
        return self._data.get('payment')

    def save(self) -> CurrentInstance:
        """
        Save the current object.

        Overrided to make sure that the payment instance and the modified flag will not change.

        Returns:
            Current instance.

        Raises:
            IliadHTTPError: On error during with the API (may be child instance of IliadHTTPError).
        """
        payment = self.payment
        modified = []

        # pylint: disable=protected-access

        if isinstance(payment, Payment):
            modified = payment._modified
            payment._modified = set()

        self._modified.add('amount')

        super().save()

        if modified and isinstance(payment, Payment):
            payment._modified = modified

        return self

    @property
    @populate_on_call
    def status(self) -> str:
        """
        Refund status.

        Returns:
            str: Current status.
        """
        return self._data.get('status')
