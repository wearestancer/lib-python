# -*- coding: utf-8 -*-

from .decorators import populate_on_call


class AbstractCountry(object):
    """Common country management."""

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def country(self) -> str:
        """
        Card, SEPA, customer, payment country.

        Returns:
            Two characters country code (ISO 3166-1 alpha-2).
        """
        return self._data.get('country')
