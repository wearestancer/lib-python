"""Test payment object"""

from stancer.status import PaymentIntentStatus
from .TestHelper import TestHelper


class TestPaymentStatus(TestHelper):
    def test_require_p_m(self):
        assert PaymentIntentStatus.REQUIRE_PAYMENT_METHOD == 'require_payment_method'
        assert PaymentIntentStatus.has_member('REQUIRE_PAYMENT_METHOD')
        assert PaymentIntentStatus.has_value('require_payment_method')

    def test_authorized(self):
        assert PaymentIntentStatus.AUTHORIZED == 'authorized'
        assert PaymentIntentStatus.has_member('AUTHORIZED')
        assert PaymentIntentStatus.has_value('authorized')

    def test_canceled(self):
        assert PaymentIntentStatus.CANCELED == 'canceled'
        assert PaymentIntentStatus.has_member('CANCELED')
        assert PaymentIntentStatus.has_value('canceled')

    def test_captured(self):
        assert PaymentIntentStatus.CAPTURED == 'captured'
        assert PaymentIntentStatus.has_member('CAPTURED')
        assert PaymentIntentStatus.has_value('captured')

    def test_unpaid(self):
        assert PaymentIntentStatus.UNPAID == 'unpaid'
        assert PaymentIntentStatus.has_member('UNPAID')
        assert PaymentIntentStatus.has_value('unpaid')

    def test_require_auth(self):
        assert PaymentIntentStatus.REQUIRE_AUTHENTICATION == 'require_authentication'
        assert PaymentIntentStatus.has_member('REQUIRE_AUTHENTICATION')
        assert PaymentIntentStatus.has_value('require_authentication')
