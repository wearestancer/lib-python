"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest
import responses

from iliad_payment import Config
from iliad_payment.core import Request
from ..stub.stub_object import StubObject
from ..TestHelper import TestHelper


class TestRequest(TestHelper):
    @responses.activate
    def test_unknown_method(self):
        obj = StubObject()
        req = Request(obj)

        assert req.plop == req
        assert len(responses.calls) == 0
