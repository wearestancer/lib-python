from typing import Optional
from stancer.card import Card

from stancer.core.decorators import populate_on_call
from stancer.core.decorators import validate_type
from stancer.exceptions import InvalidCardError


class PaymentCard(object):
    """Specific card property and method for all payments object"""

    _allowed_attributes = [
        'card',
        'method',
    ]
    _flat_attributes = [
        'card',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}
        self.id = None
        self.method = None

    @property
    @populate_on_call
    def card(self) -> Optional[Card]:
        """
        Source card for the payment intent.

        Args:
            value (Card): A valid `Card` object.

        Returns:
            Card: Card used for the payment intent.

        Raises:
            InvalidCardError: When card is invalid.
        """
        return self._data.get('card')

    @card.setter
    @validate_type(Card, throws=InvalidCardError)
    def card(self, value: Card):
        self._data['card'] = value
        self._data['method'] = 'card'
