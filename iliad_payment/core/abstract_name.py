# -*- coding: utf-8 -*-

from .decorators import populate_on_call
from .decorators import validate_type
from ..exceptions import InvalidNameError


class AbstractName(object):  # pylint: disable=too-few-public-methods
    """Commun name management."""

    _allowed_attributes = [
        'name',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def name(self) -> str:
        """
        Customer, card holder or account name.

        Args:
            value: New name, must be between 4 and 64 characters.

        Returns:
            Current defined name
        """
        return self._data.get('name')

    @name.setter
    @validate_type(str, min=4, max=64, throws=InvalidNameError)
    def name(self, value: str):
        self._data['name'] = value
