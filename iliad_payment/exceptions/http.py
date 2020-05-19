# -*- coding: utf-8 -*-

from typing import TypeVar
from requests import HTTPError, Response

from .base import IliadException

CurrentInstance = TypeVar('CurrentInstance', bound='IliadHTTPError')


class IliadHTTPError(IliadException, HTTPError):
    """
    Base exception for all HTTP exceptions raised by this module.

    They also inherit from `requests.HTTPError`.
    """

    def __new__(cls, response: Response, *args, **kwargs):
        """
        Called to create a new instance of `IliadHTTPError` or one child of it.

        Args:
            response: A `Response` object for an API call.

        Returns:
            A brand new instance waiting to get initialized with `__init__`.
        """

        exc_class = cls

        if response.status_code >= 400:
            exc_class = IliadHTTPClientError

            for tmp in IliadHTTPClientError.__subclasses__():
                if tmp.status_code == response.status_code:
                    exc_class = tmp

        if response.status_code >= 500:
            exc_class = IliadHTTPServerError

            for tmp in IliadHTTPServerError.__subclasses__():
                if tmp.status_code == response.status_code:
                    exc_class = tmp

        return super().__new__(exc_class, response, *args, **kwargs)

    def __init__(self, response: Response, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
