# -*- coding: utf-8 -*-

from .core import AbstractObject
from .core.decorators import populate_on_call


class Auth(AbstractObject):
    """Representation of an authention object."""

    _allowed_attributes = [
    ]

    @property
    @populate_on_call
    def redirect_url(self) -> str:
        """
        Redirect URL.

        Returns:
            Location of the page which will start authentication process.
        """
        return self._data.get('redirect_url')
