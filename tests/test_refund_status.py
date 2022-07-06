"""Test payment object"""

from stancer import RefundStatus
from .TestHelper import TestHelper


class TestRefundStatus(TestHelper):
    def test_not_honored(self):
        assert RefundStatus.NOT_HONORED == 'not_honored'
        assert RefundStatus.has_member('NOT_HONORED')
        assert RefundStatus.has_value('not_honored')

    def test_payment_canceled(self):
        assert RefundStatus.PAYMENT_CANCELED == 'payment_canceled'
        assert RefundStatus.has_member('PAYMENT_CANCELED')
        assert RefundStatus.has_value('payment_canceled')

    def test_refund_sent(self):
        assert RefundStatus.REFUND_SENT == 'refund_sent'
        assert RefundStatus.has_member('REFUND_SENT')
        assert RefundStatus.has_value('refund_sent')

    def test_refunded(self):
        assert RefundStatus.REFUNDED == 'refunded'
        assert RefundStatus.has_member('REFUNDED')
        assert RefundStatus.has_value('refunded')

    def test_to_refund(self):
        assert RefundStatus.TO_REFUND == 'to_refund'
        assert RefundStatus.has_member('TO_REFUND')
        assert RefundStatus.has_value('to_refund')
