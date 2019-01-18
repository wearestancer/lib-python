# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from .decorators import populate_on_call
from .decorators import validate_type


class AbstractName(object):  # pylint: disable=too-few-public-methods
    """Commun name management."""

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
    @validate_type(str, min=4, max=64)
    def name(self, value):
        self._data['name'] = value
