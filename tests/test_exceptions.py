"""Test exceptions"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import

from iliad_payment.exceptions import *  # pylint: disable=wildcard-import
from .TestHelper import TestHelper


class TestExceptions(TestHelper):
    def test_iliad_exception(self):
        assert issubclass(IliadException, Exception)

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

    def test_invalid_Iban_error(self):
        assert issubclass(InvalidIbanError, IliadValueError)

    def test_invalid_name_error(self):
        assert issubclass(InvalidNameError, IliadValueError)

    def test_invalid_payment_capture_error(self):
        assert issubclass(InvalidPaymentCaptureError, IliadTypeError)

    def test_invalid_payment_description_error(self):
        assert issubclass(InvalidPaymentDescriptionError, IliadValueError)

    def test_invalid_payment_order_id_error(self):
        assert issubclass(InvalidPaymentOrderIdError, IliadValueError)

    def test_invalid_sepa_error(self):
        assert issubclass(InvalidSepaError, IliadValueError)
