# -*- coding: utf-8 -*-


class _Singleton(type):
    """A metaclass that creates a Singleton base class when called."""

    _instances = {}

    def __call__(cls, *args, **kv):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kv)

        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """Base class for using singleton."""
