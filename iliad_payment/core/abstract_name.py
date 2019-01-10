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


class AbstractName(object):  # pylint: disable=too-few-public-methods
    """Commun name management."""

    _data = {}

    @property
    def name(self):
        """
        Customer, card holder or account name.

        Must be a string between 4 and 64 characters.
        """
        return self._data.get('name', None)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Name must be a string')

        if len(value) < 4 or len(value) > 64:
            tmp = '{} must be have at between {} and {} characters'

            raise TypeError(tmp.format('Name', 4, 64))

        self._data['name'] = value
