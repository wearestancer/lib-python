# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from builtins import str

from .decorators import populate_on_call
from .decorators import validate_type
from ..exceptions import InvalidNameError


class AbstractName(object):  # pylint: disable=too-few-public-methods
    """Commun name management."""

    _allowed_attributes = [
        'name',
    ]

    def __init__(self):
        self._data = {}

    @property
    @populate_on_call
    def name(self):
        """
        Customer, card holder or account name.

        Args:
            value (str): New name, must be between 4 and 64 characters.

        Returns:
            str: Current defined name
        """
        return self._data.get('name')

    @name.setter
    @validate_type(str, min=4, max=64, throws=InvalidNameError)
    def name(self, value):
        self._data['name'] = value
