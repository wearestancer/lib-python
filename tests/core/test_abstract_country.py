"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment.core import AbstractCountry
from ..TestHelper import TestHelper


class TestAbstractCountry(TestHelper):
    def test_country(self):
        obj = AbstractCountry()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)
