# -*- coding: utf-8 -*-

from typing import Tuple
from typing import TypeVar
from requests import HTTPError
from requests import Response

from .base import IliadException

CurrentInstance = TypeVar('CurrentInstance', bound='IliadHTTPError')


class IliadHTTPError(IliadException, HTTPError):
    """
    Base exception for all HTTP exceptions raised by this module.

    They also inherit from `requests.HTTPError`.
    """

    reason = 'HTTP error'

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
        message = type(self).reason
        type_data = None

        try:
            res = response.json()

            if response.reason is not None:
                message = response.reason

            if isinstance(res, dict) and 'error' in res:
                (message, type_data) = self._parse_message(res['error'])
        except ValueError:
            pass

        params = {
            **kwargs,
            'response': response,
        }

        super().__init__(message, *args, **params)

        self.message = message
        self.type = type_data

        if self.response is not None:
            self.reason = self.response.reason
            self.status_code = self.response.status_code

    def __str__(self) -> str:
        """
        Return a nicely printable string representation of the current error.

        This become mandatory as Python uses the first argument passed
        to `__new__` and do not update it with arguments passed to `__init__`.

        Returns:
            Current error message.
        """

        if self.message is None:
            return ''

        return str(self.message)

    @classmethod
    def _parse_message(cls, err) -> Tuple[str, str]:
        message = err
        type_data = None

        if isinstance(err, dict):
            if 'message' in err:
                message = err['message']

                if 'id' in err['message']:
                    message = str(err['message']['id'])

                if 'error' in err['message']:
                    message = err['message']['error']

                    if 'id' in err['message']:
                        message += f' ({err["message"]["id"]})'

            if 'type' in err:
                type_data = err['type']

        return (message, type_data)


class IliadHTTPClientError(IliadHTTPError):
    """Base exception for HTTP 4xx status."""

    reason = 'Client error'


class IliadHTTPServerError(IliadHTTPError):
    """Base exception for HTTP 5xx status."""

    reason = 'Server error'


class BadRequestError(IliadHTTPClientError):
    """HTTP 400 - Bad Request"""

    status_code = 400
    reason = 'Bad Request'


class UnauthorizedError(IliadHTTPClientError):
    """HTTP 401 - Unauthorized"""

    status_code = 401
    reason = 'Unauthorized'


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
