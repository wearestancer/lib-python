"""Test abstract name object"""

import pytest

from stancer.core import AbstractName
from stancer.exceptions import InvalidNameError
from ..TestHelper import TestHelper


class TestAbstractName(TestHelper):
    def test_name(self):
        obj = AbstractName()
        name = self.random_string(4, 64)

        assert obj.name is None

        obj.name = name

        assert obj.name == name

        with pytest.raises(
            InvalidNameError,
            match='Name must be a string.',
        ):
            obj.name = self.random_integer(20)

        with pytest.raises(
            InvalidNameError,
            match='Name must be between 4 and 64 characters.',
        ):
            obj.name = self.random_string(3)

        with pytest.raises(
            InvalidNameError,
            match='Name must be between 4 and 64 characters.',
        ):
            obj.name = self.random_string(65, 70)
