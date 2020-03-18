"""Test payment object"""

from datetime import date
import json
import pytest

from iliad_payment import RefundStatus
from .TestHelper import TestHelper


class TestRefundStatus(TestHelper):
    def test_not_honored(self):
        assert RefundStatus.NOT_HONORED == 'not_honored'

    def test_payment_canceled(self):
        assert RefundStatus.PAYMENT_CANCELED == 'payment_canceled'

    def test_refund_sent(self):
        assert RefundStatus.REFUND_SENT == 'refund_sent'

    def test_refunded(self):
        assert RefundStatus.REFUNDED == 'refunded'

    def test_to_refund(self):
        assert RefundStatus.TO_REFUND == 'to_refund'
