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
from .exceptions import IliadValueError


class Config(Singleton):
    """
    Handle configuration, connection and credential to API.

    To simplify configuration management, this class is a singleton.
    You can instanciate it anywhere and modify your configuration,
    it will be directly applying into the module.

    Constants:
        LIVE_MODE: Used with `Config.mode()` to set or test API mode.

        TEST_MODE: Used with `Config.mode()` to set or test API mode.
    """

    LIVE_MODE = 'live'
    TEST_MODE = 'test'

    def __init__(self):
        """Initialize configuration instance."""
        self._mode = self.TEST_MODE

        self._host = 'api.iliad78.net'
        self._port = None
        self._timeout = 5
        self._version = 1

        self.reset_keys()

    @property
    def host(self):
        """
        API host.

        Args:
            value (str): New host, default "api.iliad78.net".

        Returns:
            str: API host.
        """
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def keys(self):
        """
        API keychain.

        This module will only use secret keys (they start with "s"), but we
        allow every public as well (starting with "p").
        The module can run with only one key, if you choose the right one,
        but it is simplier to give at least your "sprod" and "stest",
        the module will choose which one to use depending your `Config.mode`
        settings.
        This way, you only have to chance the mode to be development mode.

        Args:
            value (str|(str,)): One or more keys.
                This method allows a simple string, but using tuple of strings
                is butter (as you can pass every keys in one call).
                Every keys will be tested to find public/secret and
                production/development keys.

        Returns:
            dict: Will contain "pprod", "sprod", "ptest" and "stest" keys.
        """
        return self._keys

    @keys.setter
    def keys(self, value):
        keychain = value

        if isinstance(value, str):
            keychain = (value,)

        if isinstance(value, dict):
            keychain = list(value.values())

        for key in keychain:
            if isinstance(key, str):
                key_prefix = key[:5]

                if key_prefix not in self._keys:
                    message = '"{}" is not a valid API key.'.format(key)

                    raise IliadValueError(message)

                self._keys[key_prefix] = key

    @property
    def mode(self):
        """
        API mode.

        Args:
            value (str): New mode, please use class constant.

        Returns:
            str: Actual mode.
        """
        return self._mode

    @mode.setter
    def mode(self, value):
        if value != self.LIVE_MODE and value != self.TEST_MODE:
            message = (
                'Unknonw mode "{}". '
                'Please use class constant '
                '"LIVE_MODE" or "TEST_MODE".'
            ).format(value)

            raise IliadValueError(message)

        self._mode = value

    @property
    def pprod(self):
        """
        Public production API key.

        Returns:
            str: Public production key avalaible in keychain.
        """
        return self.keys['pprod']

    @property
    def port(self):
        """
        API port.

        You may not need this, but maybe you have a weird network.

        Args:
            value (int): New port, no default (you let the http client decide).

        Returns:
            int: API port.
        """
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def ptest(self):
        """
        Public development API key.

        Returns:
            str: Public development key avalaible in keychain.
        """
        return self.keys['ptest']

    def reset_keys(self):
        """
        Reset keychain.

        Usefull for testing purpose but you may need it too.
        This will simply put every key to `None`.

        Returns:
            self: Current instance.
        """
        self._keys = {
            'pprod': None,
            'ptest': None,
            'sprod': None,
            'stest': None,
        }

        return self

    @property
    def sprod(self):
        """
        Secret production API key.

        Returns:
            str: Secret production key avalaible in keychain.
        """
        return self.keys['sprod']

    @property
    def stest(self):
        """
        Secret development API key.

        Returns:
            str: Secret development key avalaible in keychain.
        """
        return self.keys['stest']

    @property
    def timeout(self):
        """
        API timeout.

        Args:
            value (int): New timeout, default 5 seconds.

        Returns:
            int: Timeout.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def version(self):
        """
        API version.

        Not really used for now, it's just in case we need it.

        Args:
            value (int): New target API version.

        Returns:
            int: Target API version.
        """
        return self._version

    @version.setter
    def version(self, value):
        self._version = value
