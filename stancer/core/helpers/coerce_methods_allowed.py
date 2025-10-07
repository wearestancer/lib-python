# -*- coding: utf-8 -*-

from typing import Optional
from typing import Union
from typing import Any

from stancer.core.helpers.coerce_status import coerce_status
from stancer.exceptions.invalid_value import InvalidPaymentIntentMethodsAllowed
from stancer.status.method_allowed import MethodAllowed


def coerce_methods_allowed(
    value: Union[list[Any], Any, None],
) -> list[Optional[str]]:
    """
    Transform a list of enum instance into a list string.

    Args:
        value: Value to coerce.

    Returns:
        Transformed string list if value was an enum, otherwise the list directly.
    """
    if not value or value is None:
        raise InvalidPaymentIntentMethodsAllowed

    # Coerce is called before type validation.
    # If we don't check the type first we can have a type error when we try to iterate
    if not isinstance(value, list):
        value = [value]

    if len(value) <= 0 or not (
        isinstance(value[0], MethodAllowed) or MethodAllowed.has_value(str(value[0]))
    ):
        raise InvalidPaymentIntentMethodsAllowed

    return list(map(coerce_status, value))
