"""Test payment object"""

from stancer import PaymentStatus
from .TestHelper import TestHelper


class TestPaymentStatus(TestHelper):
    def test_authorize(self):
        assert PaymentStatus.AUTHORIZE == 'authorize'
        assert PaymentStatus.has_member('AUTHORIZE')
        assert PaymentStatus.has_value('authorize')

    def test_authorized(self):
        assert PaymentStatus.AUTHORIZED == 'authorized'
        assert PaymentStatus.has_member('AUTHORIZED')
        assert PaymentStatus.has_value('authorized')

    def test_canceled(self):
        assert PaymentStatus.CANCELED == 'canceled'
        assert PaymentStatus.has_member('CANCELED')
        assert PaymentStatus.has_value('canceled')

    def test_capture(self):
        assert PaymentStatus.CAPTURE == 'capture'
        assert PaymentStatus.has_member('CAPTURE')
        assert PaymentStatus.has_value('capture')

    def test_captured(self):
        assert PaymentStatus.CAPTURED == 'captured'
        assert PaymentStatus.has_member('CAPTURED')
        assert PaymentStatus.has_value('captured')

    def test_disputed(self):
        assert PaymentStatus.DISPUTED == 'disputed'
        assert PaymentStatus.has_member('DISPUTED')
        assert PaymentStatus.has_value('disputed')

    def test_expired(self):
        assert PaymentStatus.EXPIRED == 'expired'
        assert PaymentStatus.has_member('EXPIRED')
        assert PaymentStatus.has_value('expired')

    def test_failed(self):
        assert PaymentStatus.FAILED == 'failed'
        assert PaymentStatus.has_member('FAILED')
        assert PaymentStatus.has_value('failed')

    def test_to_capture(self):
        assert PaymentStatus.TO_CAPTURE == 'to_capture'
        assert PaymentStatus.has_member('TO_CAPTURE')
        assert PaymentStatus.has_value('to_capture')
