# -*- coding: utf-8 -*-

from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .exceptions import InvalidUrlError
from .status import AuthStatus


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
    def redirect_url(self) -> str:
        """
        Redirect URL.

        Returns:
            Location of the page which will start authentication process.
        """
        return self._data.get('redirect_url')

    @property
    @populate_on_call
    def return_url(self) -> str:
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
        validation=lambda v: None if v.startswith('https://') else 'Must be an HTTPS URL',
        throws=InvalidUrlError,
    )
    def return_url(self, value: str):
        self._data['return_url'] = value

    @property
    @populate_on_call
    def status(self) -> str:
        """
        Current status.

        Args:
            value: New status, you should use `AuthStatus`.

        Returns:
            Authentication status.
        """
        return self._data.get('status')
