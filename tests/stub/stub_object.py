"""Test core object"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from future import standard_library
standard_library.install_aliases()

from iliad_payment.core import AbstractObject
from iliad_payment.core.decorators import populate_on_call


class StubObject(AbstractObject):
    def force_modified(self, status):
        self._modified = status

        return self

    def force_populated(self, status):
        self._populated = status

        return self

    @property
    @populate_on_call
    def string1(self):
        return self._data.get('string1')

    @property
    @populate_on_call
    def string2(self):
        return self._data.get('string2')

    @string2.setter
    def string2(self, value):
        self._modified = True
        self._data['string2'] = value

    @property
    @populate_on_call
    def integer1(self):
        return self._data.get('integer1')

    @property
    def card1(self):
        return self._data.get('card1')
