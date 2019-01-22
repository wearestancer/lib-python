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


class AbstractCountry(object):
    """Common country management."""

    _filtered_attributes = [
        'country',
    ]

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
