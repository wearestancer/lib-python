# -*- coding: utf-8 -*-


class StancerException(Exception):
    """Base exception for all exceptions raised by this module."""


class StancerNotImplementedError(StancerException, NotImplementedError):
    """Raised when a not defined operation or function is called."""


class StancerTypeError(StancerException, TypeError):
    """Raised when an operation or function is applied with an inappropriate type."""


class StancerValueError(StancerException, ValueError):
    """Raised when an operation or function receives an inappropriate value."""


class StancerWarning(StancerException, Warning):
    """Base class for warning categories."""
