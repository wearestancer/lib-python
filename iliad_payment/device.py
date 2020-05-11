# -*- coding: utf-8 -*-

from ipaddress import ip_address

from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidIpAddressError


def ip_validation(value):
    """
    IP address validation helper.

    Not supposed to be used directly.
    """

    try:
        ip_address(value)
    except ValueError:
        return 'This IP address seems invalid (%s).'.format(value)

    return None


class Device(AbstractObject):
    """Representation of a device."""

    _allowed_attributes = [
        'city',
        'country',
        'http_accept',
        'ip',
        'languages',
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

    @property
    @populate_on_call
    def ip(self) -> str:
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
    def ip(self, value: str):
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
