"""Test core object"""

from .stub.Object import Object
from .TestHelper import TestHelper

import pytest


class TestObject(TestHelper):
    def test_id(self):
        assert Object().id is None

        id = self.random_string(29)
        obj = Object(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)
