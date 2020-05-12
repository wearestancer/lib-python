# -*- coding: utf-8 -*-

from ..decorators import populate_on_call
from ..decorators import validate_type
from ...auth import Auth
from ...device import Device
from ...exceptions import InvalidAuthError
from ...exceptions import InvalidDeviceError


class PaymentAuth(object):
    """Specific auth property and method for payment."""

    _allowed_attributes = [
        'auth',
        'device',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def auth(self) -> Auth:
        """
        Authentication request.

        Args:
            value (Auth): A valid `Auth` object.

        Returns:
            Auth: Authentication request object.

        Raises:
            InvalidAuthError: When auth is invalid.
        """
        return self._data.get('auth')

    @auth.setter
    @validate_type(Auth, throws=InvalidAuthError)
    def auth(self, value: Auth):
        self._data['auth'] = value

    @property
    @populate_on_call
    def device(self) -> Device:
        """
        Device handling the payment.

        Args:
            value (Device): A valid `Device` object.

        Returns:
            Device: Device handling the payment.

        Raises:
            InvalidDeviceError: When device is invalid.
        """
        return self._data.get('device')

    @device.setter
    @validate_type(Device, throws=InvalidDeviceError)
    def device(self, value: Device):
        self._data['device'] = value
