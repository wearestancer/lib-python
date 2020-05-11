"""Test auth object"""

import pytest
import responses

from iliad_payment import Auth
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestAuth(TestHelper):
    def test_class(self):
        assert issubclass(Auth, AbstractObject)

        attrs = Auth._get_allowed_attributes()

        assert isinstance(attrs, list)
