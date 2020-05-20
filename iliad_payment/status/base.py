# -*- coding: utf-8 -*-

from enum import Enum


class BaseStatus(Enum):
    """Base class for status."""

    def __eq__(self, value: str) -> bool:
        """Test if a status equals a value."""
        return str(self) == value

    def __str__(self) -> str:
        """Return a string representation of status."""
        return str(self.value)

    @classmethod
    def has_member(cls, member: str) -> bool:
        """Test if a key is in status."""
        return member in [item.name for item in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Test if a value is in status."""
        return value in [item.value for item in cls]

    def to_json_repr(self) -> str:
        """
        Return a string representation.

        Supposed to be use by `AbstractObject.to_json()`.

        Returns:
            Current status value.
        """
        return str(self)
