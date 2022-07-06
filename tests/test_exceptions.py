"""Test exceptions"""

import pytest

from stancer.exceptions import *  # pylint: disable=wildcard-import
from .TestHelper import TestHelper


class TestExceptions(TestHelper):
    def test_stancer_exception(self):
        assert issubclass(StancerException, Exception)

    def test_stancer_not_implemented_error(self):
        assert issubclass(StancerNotImplementedError, StancerException)
        assert issubclass(StancerNotImplementedError, NotImplementedError)

    def test_stancer_type_error(self):
        assert issubclass(StancerTypeError, StancerException)
        assert issubclass(StancerTypeError, TypeError)

    def test_stancer_value_error(self):
        assert issubclass(StancerValueError, StancerException)
        assert issubclass(StancerValueError, ValueError)

    def test_stancer_warning(self):
        assert issubclass(StancerWarning, StancerException)
        assert issubclass(StancerWarning, Warning)

    def test_invalid_amount_error(self):
        assert issubclass(InvalidAmountError, StancerValueError)

    def test_invalid_auth_error(self):
        assert issubclass(InvalidAuthError, StancerValueError)

    def test_invalid_bic_error(self):
        assert issubclass(InvalidBicError, StancerValueError)

    def test_invalid_card_error(self):
        assert issubclass(InvalidCardError, StancerValueError)

    def test_invalid_card_expiration_month_error(self):
        assert issubclass(InvalidCardExpirationMonthError, StancerValueError)

    def test_invalid_card_expiration_year_error(self):
        assert issubclass(InvalidCardExpirationYearError, StancerValueError)

    def test_invalid_card_number_error(self):
        assert issubclass(InvalidCardNumberError, StancerValueError)

    def test_invalid_card_tokenize_error(self):
        assert issubclass(InvalidCardTokenizeError, StancerTypeError)

    def test_invalid_card_verification_code_error(self):
        assert issubclass(InvalidCardVerificationCodeError, StancerValueError)

    def test_invalid_currency_error(self):
        assert issubclass(InvalidCurrencyError, StancerValueError)

    def test_invalid_customer_error(self):
        assert issubclass(InvalidCustomerError, StancerValueError)

    def test_invalid_customer_email_error(self):
        assert issubclass(InvalidCustomerEmailError, StancerValueError)

    def test_invalid_customer_external_id_error(self):
        assert issubclass(InvalidCustomerExternalIdError, StancerValueError)

    def test_invalid_customer_mobile_error(self):
        assert issubclass(InvalidCustomerMobileError, StancerValueError)

    def test_invalid_device_error(self):
        assert issubclass(InvalidDeviceError, StancerValueError)

    def test_invalid_Iban_error(self):
        assert issubclass(InvalidIbanError, StancerValueError)

    def test_invalid_ip_address_error(self):
        assert issubclass(InvalidIpAddressError, StancerValueError)

    def test_invalid_name_error(self):
        assert issubclass(InvalidNameError, StancerValueError)

    def test_invalid_payment_capture_error(self):
        assert issubclass(InvalidPaymentCaptureError, StancerTypeError)

    def test_invalid_payment_description_error(self):
        assert issubclass(InvalidPaymentDescriptionError, StancerValueError)

    def test_invalid_payment_order_id_error(self):
        assert issubclass(InvalidPaymentOrderIdError, StancerValueError)

    def test_invalid_payment_unique_id_error(self):
        assert issubclass(InvalidPaymentUniqueIdError, StancerValueError)

    def test_invalid_payment_port_error(self):
        assert issubclass(InvalidPortError, StancerValueError)

    def test_invalid_sepa_error(self):
        assert issubclass(InvalidSepaError, StancerValueError)

    def test_invalid_status_error(self):
        assert issubclass(InvalidStatusError, StancerValueError)

    def test_invalid_url_error(self):
        assert issubclass(InvalidUrlError, StancerValueError)

    def test_invalid_zip_code_error(self):
        assert issubclass(InvalidZipCodeError, StancerValueError)

    def test_missing_payment_method_error(self):
        assert issubclass(MissingPaymentMethodError, StancerValueError)

    def test_missing_api_key_error(self):
        assert issubclass(MissingApiKeyError, StancerValueError)

    def test_missing_payment_id_error(self):
        assert issubclass(MissingPaymentIdError, StancerValueError)

    def test_missing_return_url_error(self):
        assert issubclass(MissingReturnUrlError, StancerValueError)

    def test_stancer_http_error(self):
        assert issubclass(StancerHTTPError, StancerException)
        assert issubclass(StancerHTTPError, HTTPError)

    def test_stancer_http_client_error(self):
        assert issubclass(StancerHTTPClientError, StancerHTTPError)

    def test_stancer_http_server_error(self):
        assert issubclass(StancerHTTPServerError, StancerHTTPError)

    def test_bad_request_error(self):
        assert issubclass(BadRequestError, StancerHTTPClientError)
        assert BadRequestError.status_code == 400
        assert BadRequestError.reason == 'Bad Request'

    def test_not_authorized_error(self):
        assert issubclass(UnauthorizedError, StancerHTTPClientError)
        assert UnauthorizedError.status_code == 401
        assert UnauthorizedError.reason == 'Unauthorized'

    def test_payment_required_error(self):
        assert issubclass(PaymentRequiredError, StancerHTTPClientError)
        assert PaymentRequiredError.status_code == 402
        assert PaymentRequiredError.reason == 'Payment Required'

    def test_forbidden_error(self):
        assert issubclass(ForbiddenError, StancerHTTPClientError)
        assert ForbiddenError.status_code == 403
        assert ForbiddenError.reason == 'Forbidden'

    def test_not_found_error(self):
        assert issubclass(NotFoundError, StancerHTTPClientError)
        assert NotFoundError.status_code == 404
        assert NotFoundError.reason == 'Not Found'

    def test_method_not_allowed_error(self):
        assert issubclass(MethodNotAllowedError, StancerHTTPClientError)
        assert MethodNotAllowedError.status_code == 405
        assert MethodNotAllowedError.reason == 'Method Not Allowed'

    def test_not_acceptable_error(self):
        assert issubclass(NotAcceptableError, StancerHTTPClientError)
        assert NotAcceptableError.status_code == 406
        assert NotAcceptableError.reason == 'Not Acceptable'

    def test_proxy_authentication_required_error(self):
        assert issubclass(ProxyAuthenticationRequiredError, StancerHTTPClientError)
        assert ProxyAuthenticationRequiredError.status_code == 407
        assert ProxyAuthenticationRequiredError.reason == 'Proxy Authentication Required'

    def test_request_timeout_error(self):
        assert issubclass(RequestTimeoutError, StancerHTTPClientError)
        assert RequestTimeoutError.status_code == 408
        assert RequestTimeoutError.reason == 'Request Timeout'

    def test_conflict_error(self):
        assert issubclass(ConflictError, StancerHTTPClientError)
        assert ConflictError.status_code == 409
        assert ConflictError.reason == 'Conflict'

    def test_gone_error(self):
        assert issubclass(GoneError, StancerHTTPClientError)
        assert GoneError.status_code == 410
        assert GoneError.reason == 'Gone'

    def test_internal_server_error(self):
        assert issubclass(InternalServerError, StancerHTTPServerError)
        assert InternalServerError.status_code == 500
        assert InternalServerError.reason == 'Internal Server Error'

    @pytest.mark.parametrize('status_code, cls', TestHelper.http_code_provider())
    def test_factory(self, status_code, cls):
        res = Response()
        res.status_code = status_code

        req = self.random_string(20)
        res.request = req

        content = {
            'error': {
                'type': self.random_string(10),
                'message': self.random_string(10),
            },
        }

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, cls)
        assert str(obj) == content['error']['message']
        assert obj.message == content['error']['message']
        assert obj.request == req
        assert obj.response == res
        assert obj.status_code == status_code
        assert obj.type == content['error']['type']

    def test_message(self):
        res = Response()
        res.status_code = 400

        # With None

        res.json = lambda: None

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == 'Bad Request'
        assert obj.message == 'Bad Request'

        # With a string

        res.json = lambda: self.random_string(10)

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == 'Bad Request'
        assert obj.message == 'Bad Request'

        # With a JSON without error

        content = {
            'string': self.random_string(10),
        }
        expected = 'Bad Request'

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == expected
        assert obj.message == expected

        # With message

        content = {
            'error': {
                'message': self.random_string(10),
            },
        }
        expected = content['error']['message']

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == expected
        assert obj.message == expected

        # With error

        content = {
            'error': {
                'message': {
                    'error': self.random_string(10),
                },
            },
        }
        expected = content['error']['message']['error']

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == expected
        assert obj.message == expected

        # With error and id

        content = {
            'error': {
                'message': {
                    'error': self.random_string(10),
                    'id': self.random_string(10),
                },
            },
        }
        expected = '{} ({})'.format(content['error']['message']['error'], content['error']['message']['id'])

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == expected
        assert obj.message == expected

        # With only an id

        content = {
            'error': {
                'message': {
                    'id': self.random_integer(1, 10),
                },
            },
        }
        expected = str(content['error']['message']['id'])

        res.json = lambda: content

        obj = StancerHTTPError(res)

        assert isinstance(obj, BadRequestError)
        assert str(obj) == expected
        assert obj.message == expected

        # With unknown client exception

        res = Response()
        res.status_code = 499
        res.json = lambda: None

        obj = StancerHTTPError(res)

        assert isinstance(obj, StancerHTTPClientError)
        assert str(obj) == 'Client error'
        assert obj.message == 'Client error'

        # With unknown server exception

        res = Response()
        res.status_code = 599
        res.json = lambda: None

        obj = StancerHTTPError(res)

        assert isinstance(obj, StancerHTTPServerError)
        assert str(obj) == 'Server error'
        assert obj.message == 'Server error'

        # With unknown other exception

        res = Response()
        res.status_code = 399
        res.json = lambda: None

        obj = StancerHTTPError(res)

        assert isinstance(obj, StancerHTTPError)
        assert str(obj) == 'HTTP error'
        assert obj.message == 'HTTP error'
