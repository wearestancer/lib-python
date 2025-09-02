"""Test abstract object object"""

import pytest

from stancer import Config
from stancer.core import AbstractObject

from ..TestHelper import TestHelper


class TestAbstractObject(TestHelper):
    def test_id(self):
        assert AbstractObject().id is None

        uid = self.random_string(29)
        obj = AbstractObject(uid)

        assert obj.id == uid

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

        del obj.id

        assert obj.id is None

    def test__repr(self):
        obj = AbstractObject()

        assert repr(obj) == f'<AbstractObject() at 0x{id(obj):x}>'

        key1 = f'a{self.random_string(10)}'
        key2 = f'b{self.random_string(10)}'
        value1 = self.random_string(10)
        value2 = self.random_integer(1, 10)

        obj = AbstractObject(**{key2: value2, key1: value1})

        assert (
            repr(obj)
            == f'<AbstractObject({key1}="{value1}", {key2}={value2}) at 0x{id(obj):x}>'
        )

        uid = self.random_string(29)
        obj = AbstractObject(uid)

        assert repr(obj) == f'<AbstractObject("{uid}") at 0x{id(obj):x}>'

        uid = self.random_string(29)
        key1 = f'a{self.random_string(10)}'
        key2 = f'b{self.random_string(10)}'
        value1 = self.random_string(10)
        value2 = self.random_integer(1, 10)

        obj = AbstractObject(
            uid,
            **{
                key2: value2,
                key1: value1,
            },
        )

        assert (
            repr(obj)
            == f'<AbstractObject("{uid}", {key1}="{value1}", {key2}={value2}) at 0x{id(obj):x}>'
        )

    def test_uri(self):
        obj = AbstractObject()
        conf = Config()
        uid = self.random_string(29)

        assert obj.uri == 'https://api.stancer.com/v1'

        obj.hydrate(id=uid)

        assert obj.uri == f'https://api.stancer.com/v1/{uid}'

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)

        host = f'{self.random_string(25)}.{self.random_string(3)}'
        version = self.random_integer(1, 20)
        port = self.random_integer(100, 65535)

        old_host = conf.host
        old_version = conf.version

        conf.host = host
        conf.version = version

        assert obj.uri == f'https://{host}/v{version}/{uid}'
        assert obj.uri != f'https://{old_host}/v{old_version}/{uid}'

        pattern = 'https://{}:{}/v{}/{}'

        conf.port = port

        assert obj.uri == pattern.format(host, port, version, uid)

        # If defined 433 port will be shown (no exception)
        conf.port = 433

        assert obj.uri == pattern.format(host, 433, version, uid)

        # If defined 80 port will be shown (no exception)
        conf.port = 80

        assert obj.uri == pattern.format(host, 80, version, uid)

        del conf.host
        del conf.port
        del conf.version
