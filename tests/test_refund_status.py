"""Test payment object"""

from datetime import date
import json
import pytest

from iliad_payment import RefundStatus
from .TestHelper import TestHelper


class TestRefundStatus(TestHelper):
    def test_not_honored(self):
        assert RefundStatus.NOT_HONORED == 'not_honored'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(NOT_HONORED\)',
        ):
            RefundStatus.NOT_HONORED = self.random_string(10)

    def test_payment_canceled(self):
        assert RefundStatus.PAYMENT_CANCELED == 'payment_canceled'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(PAYMENT_CANCELED\)',
        ):
            RefundStatus.REFUND_SENT = self.random_string(10)

    def test_refund_sent(self):
        assert RefundStatus.REFUND_SENT == 'refund_sent'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(REFUND_SENT\)',
        ):
            RefundStatus.REFUND_SENT = self.random_string(10)

    def test_refunded(self):
        assert RefundStatus.REFUNDED == 'refunded'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(REFUNDED\)',
        ):
            RefundStatus.REFUNDED = self.random_string(10)

    def test_to_refund(self):
        assert RefundStatus.TO_REFUND == 'to_refund'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(TO_REFUND\)',
        ):
            RefundStatus.TO_REFUND = self.random_string(10)
