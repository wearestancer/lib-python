"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment.core import AbstractObject
from ..TestHelper import TestHelper


class TestAbstractObject(TestHelper):
    def test_id(self):
        assert AbstractObject().id is None

        id = self.random_string(29)
        obj = AbstractObject(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)
