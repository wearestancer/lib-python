# -*- coding: utf-8 -*-

from uuid import UUID


def coerce_uuid(value: str | UUID | None) -> str | None:
    """
    Transform UUID instance into string.

    Args:
        value: Value to coerce.

    Returns:
        Transformed string if value was an UUID, otherwise the value directly.
    """

    if isinstance(value, UUID):
        return str(value)

    return value
