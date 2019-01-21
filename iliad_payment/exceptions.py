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


class InvalidBicError(IliadValueError):
    """Raised when an invalid BIC is used."""


class InvalidCardError(IliadValueError):
    """Raised when an invalid card is used."""


class InvalidCardExpirationMonthError(IliadValueError):
    """Raised when an invalid expiration month is used."""


class InvalidCardExpirationYearError(IliadValueError):
    """Raised when an invalid expiration year is used."""


class InvalidCardNumberError(IliadValueError):
    """Raised when an invalid card number is used."""


class InvalidCardTokenizeError(IliadTypeError):
    """Raised when an invalid card tokenize status is used."""


class InvalidCardVerificationCodeError(IliadValueError):
    """Raised when an invalid CVC is used."""


class InvalidCurrencyError(IliadValueError):
    """Raised when an invalid currency is used."""


class InvalidCustomerError(IliadValueError):
    """Raised when an invalid customer is used."""


class InvalidCustomerEmailError(IliadValueError):
    """Raised when an invalid email is used."""


class InvalidCustomerMobileError(IliadValueError):
    """Raised when an invalid mobile phone number is used."""


class InvalidIbanError(IliadValueError):
    """Raised when an invalid IBAN is used."""


class InvalidNameError(IliadValueError):
    """Raised when an invalid name is used."""


class InvalidPaymentCaptureError(IliadTypeError):
    """Raised when an invalid capture is used."""


class InvalidPaymentDescriptionError(IliadValueError):
    """Raised when an invalid description is used."""


class InvalidPaymentOrderIdError(IliadValueError):
    """Raised when an invalid order ID is used."""


class InvalidSepaError(IliadValueError):
    """Raised when an invalid SEPA account is used."""


class InvalidZipCodeError(IliadValueError):
    """Raised when an invalid zip code is used."""


class MissingPaymentMethodError(IliadValueError):
    """Raised when no card or SEPA account is provided."""
