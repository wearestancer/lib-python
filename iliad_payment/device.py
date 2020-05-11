# -*- coding: utf-8 -*-

from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type


class Device(AbstractObject):
    """Representation of a device."""

    _allowed_attributes = [
        'city',
        'country',
    ]

    @property
    @populate_on_call
    def city(self) -> str:
        """
        Customer's city.

        Args:
            value: New city.

        Returns:
            Customer's city.
        """
        return self._data.get('city')

    @city.setter
    @validate_type(str)
    def city(self, value: str):
        self._data['city'] = value

    @property
    @populate_on_call
    def country(self) -> str:
        """
        Customer's country.

        Args:
            value: New country.

        Returns:
            Customer's country.
        """
        return self._data.get('country')

    @country.setter
    @validate_type(str)
    def country(self, value: str):
        self._data['country'] = value
