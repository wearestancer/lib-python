# -*- coding: utf-8 -*-


class IliadException(Exception):
    """Base exception for all exceptions raised by this module."""


class IliadNotImplementedError(IliadException, NotImplementedError):
    """Raised when a not defined operation or function is called."""


class IliadTypeError(IliadException, TypeError):
    """Raised when an operation or function is applied with an inappropriate type."""


class IliadValueError(IliadException, ValueError):
    """Raised when an operation or function receives an inappropriate value."""


class IliadWarning(IliadException, Warning):
    """Base class for warning categories."""
