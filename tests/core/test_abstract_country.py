"""Test abstract country object"""

import pytest

from stancer.core import AbstractCountry
from ..TestHelper import TestHelper


class TestAbstractCountry(TestHelper):
    def test_country(self):
        obj = AbstractCountry()

        assert obj.country is None

        with pytest.raises(AttributeError):
            obj.country = self.random_string(2)
