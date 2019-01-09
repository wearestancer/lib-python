"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *

import pytest

from iliad_payment.core import Object
from .TestHelper import TestHelper


class TestObject(TestHelper):
    def test_id(self):
        assert Object().id is None

        id = self.random_string(29)
        obj = Object(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)
