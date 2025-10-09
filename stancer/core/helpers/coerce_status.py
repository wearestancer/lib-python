# -*- coding: utf-8 -*-

from ...status.base import BaseStatus


def coerce_status(value: BaseStatus | str | None) -> str | None:
    """
    Transform a enum instance into string.

    Args:
        value: Value to coerce.

    Returns:
        Transformed string if value was an enum, otherwise the value directly.
    """

    if isinstance(value, BaseStatus):
        return str(value)

    return value
