"""Test core object"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from future import standard_library
standard_library.install_aliases()

from iliad_payment.core import AbstractObject


class StubObject(AbstractObject):
    @property
    def string1(self):
        return self._data.get('string1', None)

    @property
    def string2(self):
        return self._data.get('string2', None)

    @string2.setter
    def string2(self, value):
        self._modified = True
        self._data['string2'] = value

    @property
    def integer1(self):
        return self._data.get('integer1', None)

    @property
    def card1(self):
        return self._data.get('card1', None)
