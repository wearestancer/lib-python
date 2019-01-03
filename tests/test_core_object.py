"""Test core object"""

from iliad_payment.core import Object

import pytest
import uuid


class TestObject:
    def test_id(self):
        assert Object().id is None

        id = uuid.uuid4().hex
        obj = Object(id)

        assert obj.id == id

        with pytest.raises(AttributeError):
            obj.id = uuid.uuid4().hex
