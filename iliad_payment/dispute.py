# -*- coding: utf-8 -*-

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call


class Dispute(AbstractObject, AbstractAmount):
    """Representation of a dispute."""

    _ENDPOINT = 'disputes'

    @property
    @populate_on_call
    def order_id(self) -> str:
        """
        External order id.

        Returns:
            str: External order ID.
        """
        return self._data.get('order_id')
