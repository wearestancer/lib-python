# -*- coding: utf-8 -*-

from .base import IliadValueError


class InvalidAmountError(IliadValueError):
    """Raised when an invalid amount is used."""


class InvalidAuthError(IliadValueError):
    """Raised when an invalid auth object is used."""


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


class InvalidCardVerificationCodeError(IliadValueError):
    """Raised when an invalid CVC is used."""


class InvalidCurrencyError(IliadValueError):
    """Raised when an invalid currency is used."""


class InvalidCustomerError(IliadValueError):
    """Raised when an invalid customer is used."""


class InvalidCustomerEmailError(IliadValueError):
    """Raised when an invalid email is used."""


class InvalidCustomerExternalIdError(IliadValueError):
    """Raised when an invalid external ID is used."""


class InvalidCustomerMobileError(IliadValueError):
    """Raised when an invalid mobile phone number is used."""


class InvalidDateMandateError(IliadValueError):
    """Raised when an invalid date mandate is used."""


class InvalidDeviceError(IliadValueError):
    """Raised when an invalid device is used."""


class InvalidIbanError(IliadValueError):
    """Raised when an invalid IBAN is used."""


class InvalidIpAddressError(IliadValueError):
    """Raised when an invalid IP address is used."""


class InvalidMandateError(IliadValueError):
    """Raised when an invalid mandate is used."""


class InvalidNameError(IliadValueError):
    """Raised when an invalid name is used."""


class InvalidPaymentDescriptionError(IliadValueError):
    """Raised when an invalid description is used."""


class InvalidPaymentOrderIdError(IliadValueError):
    """Raised when an invalid order ID is used."""


class InvalidPaymentUniqueIdError(IliadValueError):
    """Raised when an invalid unique ID is used."""


class InvalidPortError(IliadValueError):
    """Raised when an invalid port is used."""


class InvalidSepaError(IliadValueError):
    """Raised when an invalid SEPA account is used."""


class InvalidStatusError(IliadValueError):
    """Raised when an invalid status is used."""


class InvalidUrlError(IliadValueError):
    """Raised when an invalid URL is used."""


class InvalidZipCodeError(IliadValueError):
    """Raised when an invalid zip code is used."""


class MissingApiKeyError(IliadValueError):
    """Raised when an action needs an API key and no one was found in keychain."""


class MissingPaymentIdError(IliadValueError):
    """Raised when an action needs a payment ID and no one was provided."""


class MissingPaymentMethodError(IliadValueError):
    """Raised when no card or SEPA account is provided."""


class MissingReturnUrlError(IliadValueError):
    """Raised when an action needs a return URL and no one was provided."""
