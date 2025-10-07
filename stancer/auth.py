# -*- coding: utf-8 -*-

from typing import Any

from .config import Config
from .core.abstract_object import AbstractObject
from .core.decorators.populate_on_call import populate_on_call
from .core.decorators.validate_type import validate_type
from .core.enum.version import Version
from .exceptions import InvalidUrlError
from .status.auth import AuthStatus


class Auth(AbstractObject):
    """Representation of an authentication object."""

    _allowed_attributes = [
        'return_url',
        'status',
    ]
    _default_values = {
        'status': AuthStatus.REQUEST,
    }

    @property
    @populate_on_call
    def redirect_url(self) -> str | None:
        """
        Redirect URL.

        Returns:
            Location of the page which will start authentication process.
        """
        return self._data.get('redirect_url')

    @property
    @populate_on_call
    def return_url(self) -> str | None:
        """
        Return URL.

        Args:
            value: New URL, must an HTTPS URL.

        Returns:
            Location of the page which will receive authentication response.
        """
        return self._data.get('return_url')

    @return_url.setter
    @validate_type(
        str,
        validation=lambda v: None
        if v.startswith('https://')
        else 'Must be an HTTPS URL',
        throws=InvalidUrlError,
    )
    def return_url(self, value: str) -> None:
        self._data['return_url'] = value

    @property
    @populate_on_call
    def status(self) -> str | None:
        """
        Current status.

        Args:
            value: New status, you should use `AuthStatus`.

        Returns:
            Authentication status.
        """
        return self._data.get('status')

    def to_json_repr(self) -> dict[str, Any] | str | bool:
        if Config().version == Version.API_V1:
            return super().to_json_repr()
        return True
