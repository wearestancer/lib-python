# -*- coding: utf-8 -*-

from ipaddress import ip_address
import os
from typing import TypeVar

from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidIpAddressError
from .exceptions import InvalidPortError


CurrentInstance = TypeVar('CurrentInstance', bound='Device')


def ip_validation(value):
    """
    IP address validation helper.

    Not supposed to be used directly.
    """

    try:
        ip_address(value)
    except ValueError:
        return f'This IP address seems invalid ({value})'

    return None


class Device(AbstractObject):
    """Representation of a device."""

    _allowed_attributes = [
        'city',
        'country',
        'http_accept',
        'ip',
        'languages',
        'port',
        'user_agent',
    ]

    @property
    @populate_on_call
    def city(self) -> str:
        """
        Customer's city.

        Args:
            value: New city.

        Returns:
            Customer's city.
        """
        return self._data.get('city')

    @city.setter
    @validate_type(str)
    def city(self, value: str):
        self._data['city'] = value

    @property
    @populate_on_call
    def country(self) -> str:
        """
        Customer's country.

        Args:
            value: New country.

        Returns:
            Customer's country.
        """
        return self._data.get('country')

    @country.setter
    @validate_type(str)
    def country(self, value: str):
        self._data['country'] = value

    @property
    @populate_on_call
    def http_accept(self) -> str:
        """
        Customer's browser acceptance.

        Args:
            value: New acceptance.

        Returns:
            Customer's browser acceptance.
        """
        return self._data.get('http_accept')

    @http_accept.setter
    @validate_type(str)
    def http_accept(self, value: str):
        self._data['http_accept'] = value

    def hydrate_from_env(self) -> CurrentInstance:
        """
        Hydrate the object using environment variables.

        You should not use this method, it's only internal plumbing.

        Returns:
            Current instance.

        Throws:
            InvalidIpAddressError: If IP address is not present.
            InvalidPortError: If port is not present.
        """

        if self.ip is None and os.getenv('SERVER_ADDR') is not None:
            self.ip = os.getenv('SERVER_ADDR')  # pylint: disable=invalid-name

        if self.port is None and os.getenv('SERVER_PORT') is not None:
            self.port = int(os.getenv('SERVER_PORT'))

        if self.http_accept is None and os.getenv('HTTP_ACCEPT') is not None:
            self.http_accept = os.getenv('HTTP_ACCEPT')

        tmp = [
            self.languages is None,
            os.getenv('HTTP_ACCEPT_LANGUAGE') is not None,
        ]

        if all(tmp):
            self.languages = os.getenv('HTTP_ACCEPT_LANGUAGE')

        tmp = [
            self.user_agent is None,
            os.getenv('HTTP_USER_AGENT') is not None,
        ]

        if all(tmp):
            self.user_agent = os.getenv('HTTP_USER_AGENT')

        if self.ip is None:
            raise InvalidIpAddressError()

        if self.port is None:
            raise InvalidPortError()

        return self

    @property
    @populate_on_call
    def ip(self) -> str:  # pylint: disable=invalid-name
        """
        Customer's IP address.

        May be an IPv4 (aka 212.27.48.10) or an IPv6 (2a01:e0c:1::1).

        Args:
            value: New IP address.

        Returns:
            Customer's IP address.
        """
        return self._data.get('ip')

    @ip.setter
    @validate_type(
        str,
        validation=ip_validation,
        throws=InvalidIpAddressError,
    )
    def ip(self, value: str): # pylint: disable=invalid-name
        self._data['ip'] = value

    @property
    @populate_on_call
    def languages(self) -> str:
        """
        Customer's browser accepted languages.

        Args:
            value: New languages.

        Returns:
            Customer's browser accepted languages.
        """
        return self._data.get('languages')

    @languages.setter
    @validate_type(str)
    def languages(self, value: str):
        self._data['languages'] = value

    @property
    @populate_on_call
    def port(self) -> int:
        """
        Customer's port.

        Args:
            value: New port.

        Returns:
            Customer's port.
        """
        return self._data.get('port')

    @port.setter
    @validate_type(
        int,
        max=65535,
        throws=InvalidPortError,
    )
    def port(self, value: int):
        self._data['port'] = value

    @property
    @populate_on_call
    def user_agent(self) -> str:
        """
        Customer's browser user agent.

        Args:
            value: New user agent.

        Returns:
            Customer's browser user agent.
        """
        return self._data.get('user_agent')

    @user_agent.setter
    @validate_type(str)
    def user_agent(self, value: str):
        self._data['user_agent'] = value
