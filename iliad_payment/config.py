# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import str

from .core.decorators import validate_type
from .core.singleton import Singleton
from .exceptions import IliadValueError


class Config(Singleton):
    """
    Handle configuration, connection and credential to API.

    To simplify configuration management, this class is a singleton.
    You can instanciate it anywhere and modify your configuration,
    it will be directly applying into the module.

    Constants:
        LIVE_MODE: Used with `Config.mode()` to set live or test API mode.
        TEST_MODE: Used with `Config.mode()` to set live or test API mode.
    """

    LIVE_MODE = 'live'  # pylint: disable=invalid-name
    TEST_MODE = 'test'  # pylint: disable=invalid-name

    def __init__(self):
        """Initialize configuration instance."""
        self._host = None
        self._keys = []
        self._mode = None
        self._port = None
        self._timeout = 0
        self._version = None

        del self.host
        del self.keys
        del self.mode
        del self.port
        del self.timeout
        del self.version

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
    @validate_type(str)
    def host(self, value):
        self._host = value

    @host.deleter
    def host(self):
        self._host = 'api.iliad78.net'

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

    @keys.deleter
    def keys(self):
        self._keys = {
            'pprod': None,
            'ptest': None,
            'sprod': None,
            'stest': None,
        }

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
    @validate_type(str)
    def mode(self, value):
        if value not in (self.LIVE_MODE, self.TEST_MODE):
            message = (
                'Unknonw mode "{}". '
                'Please use class constant '
                '"LIVE_MODE" or "TEST_MODE".'
            ).format(value)

            raise IliadValueError(message)

        self._mode = value

    @mode.deleter
    def mode(self):
        self._mode = self.TEST_MODE

    @property
    def pprod(self):
        """
        Public production API key.

        Returns:
            str: Public production key available in keychain.
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
    @validate_type(int)
    def port(self, value):
        self._port = value

    @port.deleter
    def port(self):
        self._port = None

    @property
    def ptest(self):
        """
        Public development API key.

        Returns:
            str: Public development key available in keychain.
        """
        return self.keys['ptest']

    @property
    def public_key(self):
        """
        Public API key.

        Returns:
            str: Public key available in keychain.
        """
        if self.mode == self.LIVE_MODE:
            return self.pprod

        return self.ptest

    @property
    def secret_key(self):
        """
        Secret API key.

        Returns:
            str: Secret key available in keychain.
        """
        if self.mode == self.LIVE_MODE:
            return self.sprod

        return self.stest

    @property
    def sprod(self):
        """
        Secret production API key.

        Returns:
            str: Secret production key available in keychain.
        """
        return self.keys['sprod']

    @property
    def stest(self):
        """
        Secret development API key.

        Returns:
            str: Secret development key available in keychain.
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
    @validate_type(int)
    def timeout(self, value):
        self._timeout = value

    @timeout.deleter
    def timeout(self):
        self._timeout = 5

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
    @validate_type(int)
    def version(self, value):
        self._version = value

    @version.deleter
    def version(self):
        self._version = 1
