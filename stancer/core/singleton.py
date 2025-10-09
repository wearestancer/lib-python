# -*- coding: utf-8 -*-

try:
    # Self is available in Python 3.11
    from typing import Self  # type: ignore
except ImportError:
    from typing import TypeVar

    Self = TypeVar('Self', bound='_Singleton')  # type: ignore


class _Singleton(type):
    """A metaclass that creates a Singleton base class when called."""

    _instances: dict[type[Self], Self] = {}

    def __call__(cls, *args, **kv):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kv)

        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):  # type: ignore
    """Base class for using singleton."""
