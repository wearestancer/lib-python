# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import


class IliadException(Exception):
    """Base exception for all exceptions raised by this module."""


class IliadTypeError(IliadException, TypeError):
    """
    Raised when an operation or function is applied to an object
    of inappropriate type.
    """


class IliadValueError(IliadException, ValueError):
    """
    Raised when an operation or function receives an argument
    that has the right type but an inappropriate value.
    """


class IliadWarning(IliadException, Warning):
    """Base class for warning categories."""


class InvalidAmountError(IliadValueError):
    """Raised when an invalid amount is used."""
