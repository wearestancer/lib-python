# -*- coding: utf-8 -*-

from typing import Any
from .decorators import populate_on_call


class AbstractLast4:
    """Common country management."""

    def __init__(self) -> None:
        """Init internal data."""
        self._data: dict[str, Any] = {}

    @property
    @populate_on_call
    def last4(self) -> str | None:
        """
        Card/Iban number's last 4 digits.

        Returns:
            Last 4 digits.
        """
        return self._data.get('last4')
