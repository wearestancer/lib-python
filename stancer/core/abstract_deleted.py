# -*- coding: utf-8 -*-

from typing import Optional
from .decorators import populate_on_call


class AbstractDeleted:
    """Common deleted attribute management."""

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def deleted(self) -> Optional[bool]:
        """
        If the object has been Deleted.

        Returns:
            True if the object have been deleted, False otherwise
        """
        return self._data.get('deleted')
