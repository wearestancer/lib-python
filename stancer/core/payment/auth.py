# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from ...auth import Auth
from ...device import Device
from ...exceptions import InvalidAuthError
from ...exceptions import InvalidDeviceError
from ...exceptions import StancerException
from ..decorators import populate_on_call
from ..decorators import validate_type

if TYPE_CHECKING:
    from ...payment import Payment


def _coerce_auth(value: Auth | str | bool) -> Auth | None:
    if isinstance(value, str):
        return Auth(return_url=value)

    if isinstance(value, bool):
        if value:
            return Auth()
        return None

    return value


class PaymentAuth:
    """Specific auth property and method for payment."""

    _allowed_attributes = [
        'auth',
        'device',
    ]

    def __init__(self) -> None:
        """Init internal data."""
        self._data: dict = {}
        self.id: str | None = None
        self.method = None

    @property
    @populate_on_call
    def auth(self) -> Auth | None:
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
    @validate_type(
        Auth,
        throws=InvalidAuthError,
        coerce=_coerce_auth,
    )
    def auth(self, value: Auth) -> None:
        self._data['auth'] = value

    @property
    @populate_on_call
    def device(self) -> Device | None:
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
    def device(self, value: Device) -> None:
        self._data['device'] = value

    def _create_device(self: 'Payment') -> 'Payment':  # type: ignore
        """
        Create and populate device.

        Should be used in `Payment.send()` method.
        """

        if self.method is None or self.id is not None:
            return self

        if self.device is not None:
            self.device.hydrate_from_env()

            return self

        device = Device()

        if self.auth and self.auth.return_url:
            device.hydrate_from_env()
            self.device = device
        else:
            try:
                device.hydrate_from_env()
                self.device = device
            except StancerException:
                pass

        return self
