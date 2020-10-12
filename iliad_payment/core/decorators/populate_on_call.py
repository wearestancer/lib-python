# -*- coding: utf-8 -*-

from functools import wraps


def populate_on_call(method):
    """
    Do a `populate` call before getting the value.

    This permits to get fresh data only when you need it,
    and reduce API calls.
    """
    @wraps(method)
    def wrapper(self):
        value = method(self)

        if (not value) and hasattr(self, 'populate'):
            self.populate()
            value = method(self)

        return value
    return wrapper
