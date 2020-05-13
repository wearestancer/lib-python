"""Test exceptions"""

import pytest
from requests.models import Response

from iliad_payment.exceptions import *  # pylint: disable=wildcard-import
from .TestHelper import TestHelper


class TestExceptions(TestHelper):
    def test_iliad_exception(self):
        assert issubclass(IliadException, Exception)

    def test_iliad_not_implemented_error(self):
        assert issubclass(IliadNotImplementedError, IliadException)
        assert issubclass(IliadNotImplementedError, NotImplementedError)

    def test_iliad_type_error(self):
        assert issubclass(IliadTypeError, IliadException)
        assert issubclass(IliadTypeError, TypeError)

    def test_iliad_value_error(self):
        assert issubclass(IliadValueError, IliadException)
        assert issubclass(IliadValueError, ValueError)

    def test_iliad_warning(self):
        assert issubclass(IliadWarning, IliadException)
        assert issubclass(IliadWarning, Warning)

    def test_invalid_amount_error(self):
        assert issubclass(InvalidAmountError, IliadValueError)

    def test_invalid_auth_error(self):
        assert issubclass(InvalidAuthError, IliadValueError)

    def test_invalid_bic_error(self):
        assert issubclass(InvalidBicError, IliadValueError)

    def test_invalid_card_error(self):
        assert issubclass(InvalidCardError, IliadValueError)

    def test_invalid_card_expiration_month_error(self):
        assert issubclass(InvalidCardExpirationMonthError, IliadValueError)

    def test_invalid_card_expiration_year_error(self):
        assert issubclass(InvalidCardExpirationYearError, IliadValueError)

    def test_invalid_card_number_error(self):
        assert issubclass(InvalidCardNumberError, IliadValueError)

    def test_invalid_card_tokenize_error(self):
        assert issubclass(InvalidCardTokenizeError, IliadTypeError)

    def test_invalid_card_verification_code_error(self):
        assert issubclass(InvalidCardVerificationCodeError, IliadValueError)

    def test_invalid_currency_error(self):
        assert issubclass(InvalidCurrencyError, IliadValueError)

    def test_invalid_customer_error(self):
        assert issubclass(InvalidCustomerError, IliadValueError)

    def test_invalid_customer_email_error(self):
        assert issubclass(InvalidCustomerEmailError, IliadValueError)

    def test_invalid_customer_mobile_error(self):
        assert issubclass(InvalidCustomerMobileError, IliadValueError)

    def test_invalid_device_error(self):
        assert issubclass(InvalidDeviceError, IliadValueError)

    def test_invalid_Iban_error(self):
        assert issubclass(InvalidIbanError, IliadValueError)

    def test_invalid_ip_address_error(self):
        assert issubclass(InvalidIpAddressError, IliadValueError)

    def test_invalid_name_error(self):
        assert issubclass(InvalidNameError, IliadValueError)

    def test_invalid_payment_capture_error(self):
        assert issubclass(InvalidPaymentCaptureError, IliadTypeError)

    def test_invalid_payment_description_error(self):
        assert issubclass(InvalidPaymentDescriptionError, IliadValueError)

    def test_invalid_payment_order_id_error(self):
        assert issubclass(InvalidPaymentOrderIdError, IliadValueError)

    def test_invalid_payment_port_error(self):
        assert issubclass(InvalidPortError, IliadValueError)

    def test_invalid_sepa_error(self):
        assert issubclass(InvalidSepaError, IliadValueError)

    def test_invalid_url_error(self):
        assert issubclass(InvalidUrlError, IliadValueError)

    def test_invalid_zip_code_error(self):
        assert issubclass(InvalidZipCodeError, IliadValueError)

    def test_missing_payment_method_error(self):
        assert issubclass(MissingPaymentMethodError, IliadValueError)

    def test_missing_api_key_error(self):
        assert issubclass(MissingApiKeyError, IliadValueError)

    def test_missing_payment_id_error(self):
        assert issubclass(MissingPaymentIdError, IliadValueError)

    def test_missing_return_url_error(self):
        assert issubclass(MissingReturnUrlError, IliadValueError)

    def test_iliad_http_error(self):
        assert issubclass(IliadHTTPError, IliadException)
        assert issubclass(IliadHTTPError, HTTPError)

    def test_iliad_http_client_error(self):
        assert issubclass(IliadHTTPClientError, IliadHTTPError)

    def test_iliad_http_server_error(self):
        assert issubclass(IliadHTTPServerError, IliadHTTPError)

    def test_bad_request_error(self):
        assert issubclass(BadRequestError, IliadHTTPClientError)
        assert BadRequestError.status_code == 400
        assert BadRequestError.reason == 'Bad Request'

    def test_not_authorized_error(self):
        assert issubclass(NotAuthorizedError, IliadHTTPClientError)
        assert NotAuthorizedError.status_code == 401
        assert NotAuthorizedError.reason == 'Not Authorized'

    def test_payment_required_error(self):
        assert issubclass(PaymentRequiredError, IliadHTTPClientError)
        assert PaymentRequiredError.status_code == 402
        assert PaymentRequiredError.reason == 'Payment Required'

    def test_forbidden_error(self):
        assert issubclass(ForbiddenError, IliadHTTPClientError)
        assert ForbiddenError.status_code == 403
        assert ForbiddenError.reason == 'Forbidden'

    def test_not_found_error(self):
        assert issubclass(NotFoundError, IliadHTTPClientError)
        assert NotFoundError.status_code == 404
        assert NotFoundError.reason == 'Not Found'

    def test_method_not_allowed_error(self):
        assert issubclass(MethodNotAllowedError, IliadHTTPClientError)
        assert MethodNotAllowedError.status_code == 405
        assert MethodNotAllowedError.reason == 'Method Not Allowed'

    def test_not_acceptable_error(self):
        assert issubclass(NotAcceptableError, IliadHTTPClientError)
        assert NotAcceptableError.status_code == 406
        assert NotAcceptableError.reason == 'Not Acceptable'

    def test_proxy_authentication_required_error(self):
        assert issubclass(ProxyAuthenticationRequiredError, IliadHTTPClientError)
        assert ProxyAuthenticationRequiredError.status_code == 407
        assert ProxyAuthenticationRequiredError.reason == 'Proxy Authentication Required'

    def test_request_timeout_error(self):
        assert issubclass(RequestTimeoutError, IliadHTTPClientError)
        assert RequestTimeoutError.status_code == 408
        assert RequestTimeoutError.reason == 'Request Timeout'

    def test_conflict_error(self):
        assert issubclass(ConflictError, IliadHTTPClientError)
        assert ConflictError.status_code == 409
        assert ConflictError.reason == 'Conflict'

    def test_gone_error(self):
        assert issubclass(GoneError, IliadHTTPClientError)
        assert GoneError.status_code == 410
        assert GoneError.reason == 'Gone'

    def test_internal_server_error(self):
        assert issubclass(InternalServerError, IliadHTTPServerError)
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

        obj = IliadHTTPError.factory(res)

        assert isinstance(obj, cls)
        assert obj.status_code == status_code
        assert obj.response == res
        assert obj.request == req
        assert obj.type == content['error']['type']
        assert obj.message == content['error']['message']
