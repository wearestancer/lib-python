"""Test abstract deleted object"""

import pytest

from stancer.core import AbstractDeleted
from ..TestHelper import TestHelper


class TestAbstractDeleted(TestHelper):
    def test_name(self):
        obj = AbstractDeleted()
        assert obj.deleted is None

        with pytest.raises(AttributeError):
            obj.deleted = True
