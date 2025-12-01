# -*- coding: utf-8 -*-

from typing import Optional

from ..exceptions.attribute import DeleteSetterError
from .decorators.populate_on_call import populate_on_call


class AbstractDeleted:
    """Common deleted attribute management."""

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def deleted(self) -> Optional[bool]:
        """
        Is the object deleted?

        Returns:
            True is the object have been deleted, False otherwise
        """
        return self._data.get('deleted')

    @deleted.setter
    def deleted(self, value: None) -> None:
        raise DeleteSetterError
