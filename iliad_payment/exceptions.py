# -*- coding: utf-8 -*-

from requests import HTTPError, Response
from typing import TypeVar

CurrentInstance = TypeVar('CurrentInstance', bound='IliadHTTPError')


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


# HTTP Errors

class IliadHTTPError(IliadException, HTTPError):
    """
    Base exception for all HTTP exceptions raised by this module.

    They also inherit from `requests.HTTPError`.
    """

    def __init__(self, response: Response, *args, **kwargs):
        super(IliadHTTPError, self).__init__(*args, **kwargs)

        self.response = response
        self.status_code = response.status_code

        if hasattr(response, 'reason'):
            self.reason = getattr(response, 'reason')

        self.request = getattr(response, 'request')

        self.type = ''
        self.message = ''

        try:
            res = response.json()

            if 'error' in res:
                if 'type' in res['error']:
                    self.type = res['error']['type']

                if 'message' in res['error']:
                    self.message = res['error']['message']
        except ValueError:
            pass

    @classmethod
    def factory(cls, response: Response, *args, **kwargs) -> CurrentInstance:
        """
        Return correct error instance form HTTP status.

        Args:
            response: HTTP Response that produced the exception
            *args: Variable lenght argument list, will passed to the new instance.
            **kwargs: Arbitrary keywors arguments, will passed to the new instance.

        Returns:
            An child instance of IliadHTTPError.
        """
        if response.status_code >= 500:
            for tmp in IliadHTTPServerError.__subclasses__():
                if tmp.status_code == response.status_code:
                    return tmp(response, *args, **kwargs)

            return IliadHTTPServerError(response, *args, **kwargs)

        if response.status_code >= 400:
            for tmp in IliadHTTPClientError.__subclasses__():
                if tmp.status_code == response.status_code:
                    return tmp(response, *args, **kwargs)

            return IliadHTTPClientError(response, *args, **kwargs)

        return IliadHTTPError(response, *args, **kwargs)


class IliadHTTPClientError(IliadHTTPError):
    """Base exception for HTTP 4xx status."""


class IliadHTTPServerError(IliadHTTPError):
    """Base exception for HTTP 5xx status."""


class BadRequestError(IliadHTTPClientError):
    """HTTP 400 - Bad Request"""

    status_code = 400
    reason = 'Bad Request'


class NotAuthorizedError(IliadHTTPClientError):
    """HTTP 401 - Not Authorized"""

    status_code = 401
    reason = 'Not Authorized'


class PaymentRequiredError(IliadHTTPClientError):
    """HTTP 402 - Payment Required"""

    status_code = 402
    reason = 'Payment Required'


class ForbiddenError(IliadHTTPClientError):
    """HTTP 403 - Forbidden"""

    status_code = 403
    reason = 'Forbidden'


class NotFoundError(IliadHTTPClientError):
    """HTTP 404 - Not Found"""

    status_code = 404
    reason = 'Not Found'


class MethodNotAllowedError(IliadHTTPClientError):
    """HTTP 405 - Method Not Allowed"""

    status_code = 405
    reason = 'Method Not Allowed'


class NotAcceptableError(IliadHTTPClientError):
    """HTTP 406 - Not Acceptable"""

    status_code = 406
    reason = 'Not Acceptable'


class ProxyAuthenticationRequiredError(IliadHTTPClientError):
    """HTTP 407 - Proxy Authentication Required"""

    status_code = 407
    reason = 'Proxy Authentication Required'


class RequestTimeoutError(IliadHTTPClientError):
    """HTTP 408 - Request Timeout"""

    status_code = 408
    reason = 'Request Timeout'


class ConflictError(IliadHTTPClientError):
    """HTTP 409 - Conflict"""

    status_code = 409
    reason = 'Conflict'


class GoneError(IliadHTTPClientError):
    """HTTP 410 - Gone"""

    status_code = 410
    reason = 'Gone'


class InternalServerError(IliadHTTPServerError):
    """HTTP 500 - Internal Server Error"""

    status_code = 500
    reason = 'Internal Server Error'
