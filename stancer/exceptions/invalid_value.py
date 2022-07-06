# -*- coding: utf-8 -*-

from .base import StancerValueError


class InvalidAmountError(StancerValueError):
    """Raised when an invalid amount is used."""


class InvalidAuthError(StancerValueError):
    """Raised when an invalid auth object is used."""


class InvalidBicError(StancerValueError):
    """Raised when an invalid BIC is used."""


class InvalidCardError(StancerValueError):
    """Raised when an invalid card is used."""


class InvalidCardExpirationMonthError(StancerValueError):
    """Raised when an invalid expiration month is used."""


class InvalidCardExpirationYearError(StancerValueError):
    """Raised when an invalid expiration year is used."""


class InvalidCardNumberError(StancerValueError):
    """Raised when an invalid card number is used."""


class InvalidCardVerificationCodeError(StancerValueError):
    """Raised when an invalid CVC is used."""


class InvalidCurrencyError(StancerValueError):
    """Raised when an invalid currency is used."""


class InvalidCustomerError(StancerValueError):
    """Raised when an invalid customer is used."""


class InvalidCustomerEmailError(StancerValueError):
    """Raised when an invalid email is used."""


class InvalidCustomerExternalIdError(StancerValueError):
    """Raised when an invalid external ID is used."""


class InvalidCustomerMobileError(StancerValueError):
    """Raised when an invalid mobile phone number is used."""


class InvalidDateMandateError(StancerValueError):
    """Raised when an invalid date mandate is used."""


class InvalidDeviceError(StancerValueError):
    """Raised when an invalid device is used."""


class InvalidIbanError(StancerValueError):
    """Raised when an invalid IBAN is used."""


class InvalidIpAddressError(StancerValueError):
    """Raised when an invalid IP address is used."""


class InvalidMandateError(StancerValueError):
    """Raised when an invalid mandate is used."""


class InvalidNameError(StancerValueError):
    """Raised when an invalid name is used."""


class InvalidPaymentDescriptionError(StancerValueError):
    """Raised when an invalid description is used."""


class InvalidPaymentOrderIdError(StancerValueError):
    """Raised when an invalid order ID is used."""


class InvalidPaymentUniqueIdError(StancerValueError):
    """Raised when an invalid unique ID is used."""


class InvalidPortError(StancerValueError):
    """Raised when an invalid port is used."""


class InvalidSearchFilter(StancerValueError):
    """Raised when an invalid search filter is used."""


class InvalidSearchResponse(StancerValueError):
    """Raised when server provide an invalid search response."""


class InvalidSepaError(StancerValueError):
    """Raised when an invalid SEPA account is used."""


class InvalidStatusError(StancerValueError):
    """Raised when an invalid status is used."""


class InvalidUrlError(StancerValueError):
    """Raised when an invalid URL is used."""


class InvalidZipCodeError(StancerValueError):
    """Raised when an invalid zip code is used."""


class MissingApiKeyError(StancerValueError):
    """Raised when an action needs an API key and no one was found in keychain."""


class MissingPaymentIdError(StancerValueError):
    """Raised when an action needs a payment ID and no one was provided."""


class MissingPaymentMethodError(StancerValueError):
    """Raised when no card or SEPA account is provided."""


class MissingReturnUrlError(StancerValueError):
    """Raised when an action needs a return URL and no one was provided."""
