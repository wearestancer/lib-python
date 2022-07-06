"""Test config object"""

import datetime
import pytest
from pytz import timezone

from stancer import Config
from stancer.exceptions import StancerValueError
from .TestHelper import TestHelper


class TestConfig(TestHelper):
    def test_class(self):
        assert Config() == Config()

    def test_default_timezone(self):
        obj = Config()
        tz = timezone('Europe/Paris')

        assert isinstance(obj.default_timezone, datetime.tzinfo)
        assert obj.default_timezone == datetime.timezone.utc

        obj.default_timezone = tz

        assert obj.default_timezone is tz

        del obj.default_timezone

        assert isinstance(obj.default_timezone, datetime.tzinfo)
        assert obj.default_timezone == datetime.timezone.utc

    def test_host(self):
        obj = Config()
        host = self.random_string(15) + '.' + self.random_string(2)

        assert obj.host == 'api.stancer.com'

        obj.host = host

        assert obj.host == host

        # Delete will put it on default
        del obj.host

        assert obj.host == 'api.stancer.com'

    def test_keys(self):
        obj = Config()
        pprod = 'pprod_' + self.random_string(24)
        sprod = 'sprod_' + self.random_string(24)
        ptest = 'ptest_' + self.random_string(24)
        stest = 'stest_' + self.random_string(24)

        # test setup add a stest key, we will put back after this test
        previous_keys = obj.keys
        del obj.keys

        assert obj.pprod is None
        assert obj.sprod is None
        assert obj.ptest is None
        assert obj.stest is None
        assert isinstance(obj.keys, dict)

        keys = obj.keys

        assert 'pprod' in keys
        assert keys['pprod'] is None
        assert 'sprod' in keys
        assert keys['sprod'] is None
        assert 'ptest' in keys
        assert keys['ptest'] is None
        assert 'stest' in keys
        assert keys['stest'] is None

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

        keychain = {
            'pprod': 'pprod_' + self.random_string(24),
            'sprod': 'sprod_' + self.random_string(24),
            'ptest': 'ptest_' + self.random_string(24),
            'stest': 'stest_' + self.random_string(24),
        }

        obj.keys = keychain

        assert obj.pprod == keychain['pprod']
        assert obj.sprod == keychain['sprod']
        assert obj.ptest == keychain['ptest']
        assert obj.stest == keychain['stest']

        bad_key = self.random_string(30)

        with pytest.raises(
            StancerValueError,
            match='"{}" is not a valid API key.'.format(bad_key),
        ):
            obj.keys = bad_key

        del obj.keys
        obj.keys = previous_keys

    def test_mode(self):
        obj = Config()
        mode = self.random_string(5)

        assert obj.mode == Config.TEST_MODE

        obj.mode = Config.LIVE_MODE

        assert obj.mode == Config.LIVE_MODE

        message = (
            'Unknonw mode "{}". '
            'Please use class constant "LIVE_MODE" or "TEST_MODE".'
        ).format(mode)

        with pytest.raises(
            StancerValueError,
            match=message,
        ):
            obj.mode = mode

        # Delete will put it on default
        del obj.mode

        assert obj.mode == Config.TEST_MODE

    def test_port(self):
        obj = Config()
        port = self.random_integer(100, 65535)

        assert obj.port is None

        obj.port = port

        assert obj.port == port

        # Delete will put it on default
        del obj.port

        assert obj.port is None

    def test_public_key(self):
        obj = Config()
        pprod = 'pprod_' + self.random_string(24)
        sprod = 'sprod_' + self.random_string(24)
        ptest = 'ptest_' + self.random_string(24)
        stest = 'stest_' + self.random_string(24)

        # test setup add a stest key, we will put back after this test
        previous_keys = obj.keys
        del obj.keys

        obj.keys = (ptest, stest, pprod, sprod)

        assert obj.mode == Config.TEST_MODE
        assert obj.public_key == ptest

        obj.mode = Config.LIVE_MODE

        assert obj.public_key == pprod

        obj.mode = Config.TEST_MODE

        del obj.keys
        obj.keys = previous_keys

    @pytest.mark.parametrize(
        'key, mode, prefix',
        TestHelper.api_key_provider(),
    )
    def test_reset_keys(self, key, mode, prefix):
        obj = Config()

        previous_keys = obj.keys
        prefixes = [
            'pprod',
            'sprod',
            'ptest',
            'stest',
        ]

        del obj.keys

        for key_prefix in prefixes:
            assert getattr(obj, key_prefix) is None

        obj.keys = key

        assert getattr(obj, prefix) == key

        for key_prefix in prefixes:
            if key_prefix != prefix:
                assert getattr(obj, key_prefix) is None

        # reset
        del obj.keys
        obj.keys = previous_keys

    def test_secret_key(self):
        obj = Config()
        pprod = 'pprod_' + self.random_string(24)
        sprod = 'sprod_' + self.random_string(24)
        ptest = 'ptest_' + self.random_string(24)
        stest = 'stest_' + self.random_string(24)

        # test setup add a stest key, we will put back after this test
        previous_keys = obj.keys
        del obj.keys
        del obj.mode

        obj.keys = (ptest, stest, pprod, sprod)

        assert obj.mode == Config.TEST_MODE
        assert obj.secret_key == stest

        obj.mode = Config.LIVE_MODE

        assert obj.secret_key == sprod

        obj.mode = Config.TEST_MODE

        del obj.keys
        obj.keys = previous_keys

    def test_timeout(self):
        obj = Config()
        timeout = self.random_integer(1, 1000)

        assert obj.timeout is None

        obj.timeout = timeout

        assert obj.timeout == timeout

        # Delete will put it on default
        del obj.timeout

        assert obj.timeout is None

    def test_version(self):
        obj = Config()
        version = self.random_integer(1, 20)

        assert obj.version == 1

        obj.version = version

        assert obj.version == version

        # Delete will put it on default
        del obj.version

        assert obj.version == 1
