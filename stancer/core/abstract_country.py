# -*- coding: utf-8 -*-

from .decorators import populate_on_call


class AbstractCountry:
    """Common country management."""

    def __init__(self) -> None:
        """Init internal data."""
        self._data: dict = {}

    @property
    @populate_on_call
    def country(self) -> str | None:
        """
        Card, SEPA, customer, payment country.

        Returns:
            Two characters country code (ISO 3166-1 alpha-2).
        """
        return self._data.get('country')
