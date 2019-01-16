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

    def test_keys(self):
        obj = Config()
        pprod = 'pprod_' + self.random_string(24)
        sprod = 'sprod_' + self.random_string(24)
        ptest = 'ptest_' + self.random_string(24)
        stest = 'stest_' + self.random_string(24)

        assert obj.pprod is None
        assert obj.sprod is None
        assert obj.ptest is None
        assert obj.stest is not None  # test setup add a stest key
        assert isinstance(obj.keys, dict)

        keys = obj.keys

        assert 'pprod' in keys
        assert keys['pprod'] is None
        assert 'sprod' in keys
        assert keys['sprod'] is None
        assert 'ptest' in keys
        assert keys['ptest'] is None
        assert 'stest' in keys
        assert keys['stest'] is not None

        obj.keys = stest

        assert obj.pprod is None
        assert obj.sprod is None
        assert obj.ptest is None
        assert obj.stest == stest
        assert isinstance(obj.keys, dict)

        keys = obj.keys

        assert 'pprod' in keys
        assert keys['pprod'] is None
        assert 'sprod' in keys
        assert keys['sprod'] is None
        assert 'ptest' in keys
        assert keys['ptest'] is None
        assert 'stest' in keys
        assert keys['stest'] == stest

        obj.keys = (ptest, pprod)

        assert obj.pprod == pprod
        assert obj.sprod is None
        assert obj.ptest == ptest
        assert obj.stest == stest
        assert isinstance(obj.keys, dict)

        keys = obj.keys

        assert 'pprod' in keys
        assert keys['pprod'] == pprod
        assert 'sprod' in keys
        assert keys['sprod'] is None
        assert 'ptest' in keys
        assert keys['ptest'] == ptest
        assert 'stest' in keys
        assert keys['stest'] == stest

        obj.keys = (ptest, stest, pprod, sprod)

        assert obj.pprod == pprod
        assert obj.sprod == sprod
        assert obj.ptest == ptest
        assert obj.stest == stest
        assert isinstance(obj.keys, dict)

        keys = obj.keys

        assert 'pprod' in keys
        assert keys['pprod'] == pprod
        assert 'sprod' in keys
        assert keys['sprod'] == sprod
        assert 'ptest' in keys
        assert keys['ptest'] == ptest
        assert 'stest' in keys
        assert keys['stest'] == stest

        key1 = 'sprod_' + self.random_string(24)
        key2 = 'sprod_' + self.random_string(24)

        obj.keys = (key1, key2)

        assert obj.sprod == key2

        bad_key = self.random_string(30)

        with pytest.raises(
            TypeError,
            match='"{}" is not a valid API key.'.format(bad_key),
        ):
            obj.keys = bad_key

    def test_mode(self):
        obj = Config()
        mode = self.random_string(5)

        assert obj.mode == Config.TEST_MODE

        obj.mode = Config.LIVE_MODE

        assert obj.mode == Config.LIVE_MODE

        message = 'Unknonw mode "{}". '
        'Please use class constant "LIVE_MODE" or "TEST_MODE".'.format(mode)

        with pytest.raises(
            TypeError,
            match=message,
        ):
            obj.mode = mode

        obj.mode = Config.TEST_MODE

    def test_port(self):
        obj = Config()
        port = self.random_integer(100, 65535)

        assert obj.port is None

        old_port = obj.port
        obj.port = port

        assert obj.port == port

        obj.port = old_port

    def test_timeout(self):
        obj = Config()
        timeout = self.random_integer(1, 1000)

        assert obj.timeout == 5

        old_timeout = obj.timeout
        obj.timeout = timeout

        assert obj.timeout == timeout

        obj.timeout = old_timeout

    def test_version(self):
        obj = Config()
        version = self.random_integer(1, 20)

        assert obj.version == 1

        old_version = obj.version
        obj.version = version

        assert obj.version == version

        obj.version = old_version
