# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import TYPE_CHECKING

from .payment_protocol import PaymentProtocol
from ...exceptions import InvalidAmountError
from ...status.refund import RefundStatus
from ..decorators import populate_on_call
from ..decorators import validate_type

if TYPE_CHECKING:
    from ...refund import Refund


class PaymentRefund(ABC, PaymentProtocol):
    """Specific property and method for payment refunds."""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @property
    def _init_refunds(self):
        # Prevent import loop
        from ...refund import Refund  # pylint: disable=import-outside-toplevel

        return Refund

    @validate_type(
        int,
        min=50,
        throws=InvalidAmountError,
        optional=True,
        silent=True,
    )
    def refund(self, amount: int = 0):
        """
        Refund a payment, or part of it.

        Args:
            amount (int): Amount to refund,
                if not present all paid amount will be refund.

        Raises:
            InvalidAmountError: When trying to refund more than paid.
            InvalidAmountError: When the amount is invalid.
        """
        from ...refund import Refund  # pylint: disable=import-outside-toplevel

        refund = Refund()
        params: dict[str, Any] = {
            'payment': self,
        }
        if amount:
            if amount > self.refundable_amount:
                currency = self.currency.upper() if self.currency else ''
                message = (
                    f'You are trying to refund ({amount / 100:.2f} {currency}) '
                    f'more than possible ({self.refundable_amount / 100:.2f} '
                    f'{currency}).'
                )

                raise InvalidAmountError(message)

            params['amount'] = amount

        refund.hydrate(**params)
        refund.send()

        refunds = self._data.get('refunds', [])
        refunds.append(refund)

        self._data['refunds'] = refunds

        if refund.status != RefundStatus.TO_REFUND:
            self._populated = False
            self.populate()

        return refund

    @property
    def refunded_amount(self) -> int:
        """
        Amount already refunded.

        Returns:
            int: Amount already refund.
        """
        return sum(map(lambda refund: refund.amount, self.refunds))

    @property
    def refundable_amount(self) -> int:
        """
        Amount not already refunded.

        Returns:
            int: Amount left to refund.
        """
        if self.amount is None or self.refunded_amount is None:
            raise InvalidAmountError
        return self.amount - self.refunded_amount

    @property
    @populate_on_call
    def refunds(self) -> list['Refund']:
        """
        Returns refund's list.

        Returns:
            Refund[]: Refund's list
        """
        return self._data.get('refunds', [])
