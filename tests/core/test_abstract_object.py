"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import pytest

from iliad_payment import Config
from iliad_payment.core import AbstractObject
from ..TestHelper import TestHelper


class TestAbstractObject(TestHelper):
    def test_id(self):
        assert AbstractObject().id is None

        uid = self.random_string(29)
        obj = AbstractObject(uid)

        assert obj.id == uid

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_uri(self):
        obj = AbstractObject()
        conf = Config()
        uid = self.random_string(29)

        assert obj.uri == 'https://api.iliad78.net/v1'

        obj.hydrate({'id': uid})

        assert obj.uri == 'https://api.iliad78.net/v1/' + uid

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)

        host = self.random_string(25) + '.' + self.random_string(3)
        version = self.random_integer(1, 20)

        old_host = conf.host
        old_version = conf.version

        conf.host = host
        conf.version = version

        assert obj.uri == 'https://{}/v{}/{}'.format(host, version, uid)

        conf.host = old_host
        conf.version = old_version
