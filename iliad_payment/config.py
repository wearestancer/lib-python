# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from .core.singleton import Singleton


class Config(Singleton):
    """Handle configuration, connection and credential to API"""

    LIVE_MODE = 'live'
    TEST_MODE = 'test'

    def __init__(self):
        self._mode = self.TEST_MODE

        self._host = 'api.iliad78.net'
        self._port = None
        self._timeout = 5
        self._version = 1

        self._keys = {
            'pprod': None,
            'ptest': None,
            'sprod': None,
            'stest': None,
        }

    @property
    def host(self):
        """API host."""
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def keys(self):
        """API key chain."""
        return self._keys

    @keys.setter
    def keys(self, value):
        keychain = value

        if isinstance(value, str):
            keychain = (value,)

        for key in keychain:
            key_prefix = key[:5]

            if key_prefix not in self._keys:
                raise TypeError('"{}" is not a valid API key.'.format(key))

            self._keys[key_prefix] = key

    @property
    def mode(self):
        """API mode."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if value != self.LIVE_MODE and value != self.TEST_MODE:
            message = 'Unknonw mode "{}". '
            'Please use class constant '
            '"LIVE_MODE" or "TEST_MODE".'.format(value)

            raise TypeError(message)

        self._mode = value

    @property
    def pprod(self):
        """Public production API key."""
        return self.keys['pprod']

    @property
    def port(self):
        """API port."""
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def ptest(self):
        """Public development API key."""
        return self.keys['ptest']

    @property
    def sprod(self):
        """Secret production API key."""
        return self.keys['sprod']

    @property
    def stest(self):
        """Secret development API key."""
        return self.keys['stest']

    @property
    def timeout(self):
        """API timeout."""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def version(self):
        """API version."""
        return self._version

    @version.setter
    def version(self, value):
        self._version = value
