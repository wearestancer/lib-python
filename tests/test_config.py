"""Test config object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment import Config
from .TestHelper import TestHelper


class TestConfig(TestHelper):
    def test_class(self):
        assert Config() == Config()

    def test_host(self):
        obj = Config()
        host = self.random_string(15) + '.' + self.random_string(2)

        assert obj.host == 'api.iliad78.net'

        old_host = obj.host
        obj.host = host

        assert obj.host == host

        obj.host = old_host

    def test_version(self):
        obj = Config()
        version = self.random_integer(1, 20)

        assert obj.version == 1

        old_version = obj.version
        obj.version = version

        assert obj.version == version

        obj.version = old_version
