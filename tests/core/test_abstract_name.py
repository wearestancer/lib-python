"""Test abstract name object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment.core import AbstractName
from iliad_payment.exceptions import InvalidNameError
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
