# -*- coding: utf-8 -*-

from typing import Optional
from typing import Union

from ...status.base import BaseStatus


def coerce_status(value: Optional[Union[BaseStatus, str]]) -> Optional[str]:
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
