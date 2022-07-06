# -*- coding: utf-8 -*-

from ..decorators import populate_on_call
from ..decorators import validate_type
from ...exceptions import InvalidAmountError
from ...status.refund import RefundStatus


class PaymentRefund(object):
    """Specific property and method for payment refunds."""

    _allowed_attributes = [
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}
        self.amount = None
        self.currency = None
        self.populate = lambda: None
        self._populated = None

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
        # Prevent import loop
        from ...refund import Refund  # pylint: disable=import-outside-toplevel

        refund = Refund()
        params = {
            'payment': self,
        }

        if amount:
            if amount > self.refundable_amount:
                message = (
                    'You are trying to refund ({amount:.2f} {currency}) '
                    'more than possible ({max:.2f} {currency}).'
                ).format(
                    amount=amount / 100,
                    currency=self.currency.upper(),
                    max=self.refundable_amount / 100,
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
        return self.amount - self.refunded_amount

    @property
    @populate_on_call
    def refunds(self):
        """
        Returns refund's list.

        Returns:
            Refund[]: Refund's list
        """
        return self._data.get('refunds', [])
