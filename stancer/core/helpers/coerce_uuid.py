# -*- coding: utf-8 -*-

from typing import Optional
from typing import Union
from uuid import UUID


def coerce_uuid(value: Optional[Union[str, UUID]]) -> Optional[str]:
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
