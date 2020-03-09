"""Test payment object"""

from datetime import date
import json
import pytest

from iliad_payment import PaymentStatus
from .TestHelper import TestHelper


class TestPaymentStatus(TestHelper):
    def test_authorize(self):
        assert PaymentStatus.AUTHORIZE == 'authorize'

    def test_authorized(self):
        assert PaymentStatus.AUTHORIZED == 'authorized'

    def test_canceled(self):
        assert PaymentStatus.CANCELED == 'canceled'

    def test_capture(self):
        assert PaymentStatus.CAPTURE == 'capture'

    def test_captured(self):
        assert PaymentStatus.CAPTURED == 'captured'

    def test_disputed(self):
        assert PaymentStatus.DISPUTED == 'disputed'

    def test_expired(self):
        assert PaymentStatus.EXPIRED == 'expired'

    def test_failed(self):
        assert PaymentStatus.FAILED == 'failed'

    def test_to_capture(self):
        assert PaymentStatus.TO_CAPTURE == 'to_capture'
