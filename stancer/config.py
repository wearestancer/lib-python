# -*- coding: utf-8 -*-
from datetime import timezone

from .core.singleton import Singleton
from .exceptions import StancerValueError


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

    def __init__(self) -> None:
        """Initialize configuration instance."""
        self._default_timezone = timezone.utc
        self._host: str | None = None
        self._keys: dict[str, str | None] = {}
        self._mode: str | None = None
        self._port: int | None = None
        self._timeout: int | None = None
        self._version: int | None = None

        del self.host
        del self.keys
        del self.mode
        del self.port
        del self.timeout
        del self.version

    @property
    def default_timezone(self) -> timezone:
        """
        Will be used as default time zone for every datetime object created by the API.

        Args:
            tz: New time zone.

        Returns:
            str: Default time zone
        """
        return self._default_timezone

    @default_timezone.setter
    def default_timezone(self, zone: timezone) -> None:
        self._default_timezone = zone

    @default_timezone.deleter
    def default_timezone(self) -> None:
        self._default_timezone = timezone.utc

    @property
    def host(self) -> str | None:
        """
        API host.

        Args:
            value: New host, default "api.stancer.com".

        Returns:
            API host.
        """
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        self._host = value

    @host.deleter
    def host(self) -> None:
        self._host = 'api.stancer.com'

    @property
    def keys(self) -> dict[str, str | None]:
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
            value: One or more keys.
                This method allows a simple string, but using tuple of strings
                is butter (as you can pass every keys in one call).
                Every keys will be tested to find public/secret and
                production/development keys.

        Returns:
            Will contain "pprod", "sprod", "ptest" and "stest" keys.

        Raises:
            StancerValueError: When a key is not valid.
        """
        return self._keys

    @keys.setter
    def keys(self, value: list[str] | str):
        keychain: list[str] | str | tuple[str, ...] = value

        if isinstance(value, str):
            keychain = (value,)

        if isinstance(value, dict):
            keychain = list(value.values())

        for key in keychain:
            if isinstance(key, str):
                key_prefix = key[:5]

                if key_prefix not in self._keys:
                    raise StancerValueError(f'"{key}" is not a valid API key.')
                self._keys[key_prefix] = key

    @keys.deleter
    def keys(self) -> None:
        self._keys = {
            'pprod': None,
            'ptest': None,
            'sprod': None,
            'stest': None,
        }

    @property
    def mode(self) -> str | None:
        """
        API mode.

        Args:
            value: New mode, please use class constant.

        Returns:
            Actual mode.

        Raises:
            StancerValueError: If ``mode`` is not one of class contant.
        """
        return self._mode

    @mode.setter
    def mode(self, value: str) -> None:
        if value not in (self.LIVE_MODE, self.TEST_MODE):
            message = ' '.join(
                [
                    f'Unknown mode "{value}".',
                    'Please use class constant "LIVE_MODE" or "TEST_MODE".',
                ]
            )

            raise StancerValueError(message)

        self._mode = value

    @mode.deleter
    def mode(self):
        self._mode = self.TEST_MODE

    @property
    def pprod(self) -> str | None:
        """
        Public production API key.

        Returns:
            Public production key available in keychain.
        """
        return self.keys['pprod']

    @property
    def port(self) -> int | None:
        """
        API port.

        You may not need this, but maybe you have a weird network.

        Args:
            value: New port, no default (you let the http client decide).

        Returns:
            API port.
        """
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        self._port = value

    @port.deleter
    def port(self) -> None:
        self._port = None

    @property
    def ptest(self) -> str | None:
        """
        Public development API key.

        Returns:
            Public development key available in keychain.
        """
        return self.keys['ptest']

    @property
    def public_key(self) -> str | None:
        """
        Public API key.

        Returns:
            Public key available in keychain.
        """
        if self.mode == self.LIVE_MODE:
            return self.pprod

        return self.ptest

    @property
    def secret_key(self) -> str | None:
        """
        Secret API key.

        Returns:
            Secret key available in keychain.
        """
        if self.mode == self.LIVE_MODE:
            return self.sprod

        return self.stest

    @property
    def sprod(self) -> str | None:
        """
        Secret production API key.

        Returns:
            Secret production key available in keychain.
        """
        return self.keys['sprod']

    @property
    def stest(self) -> str | None:
        """
        Secret development API key.

        Returns:
            Secret development key available in keychain.
        """
        return self.keys['stest']

    @property
    def timeout(self) -> int | None:
        """
        API timeout.

        Args:
            value: New timeout, default taken from the requests lib.

        Returns:
            Timeout.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self._timeout = value

    @timeout.deleter
    def timeout(self) -> None:
        self._timeout = None

    @property
    def version(self) -> int | None:
        """
        API version.

        Not really used for now, it's just in case we need it.

        Args:
            value: New target API version.

        Returns:
            Target API version.
        """
        return self._version

    @version.setter
    def version(self, value: int) -> None:
        self._version = value

    @version.deleter
    def version(self) -> None:
        self._version = 1
