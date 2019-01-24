# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from .decorators import populate_on_call


class AbstractCountry(object):
    """Common country management."""

    def __init__(self):
        self._data = {}

    @property
    @populate_on_call
    def country(self):
        """
        Card, SEPA, customer, payment country.

        Returns:
            str: Two characters country code (ISO 3166-1 alpha-2).
        """
        return self._data.get('country')
