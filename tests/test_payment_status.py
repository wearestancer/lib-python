"""Test payment object"""

from datetime import date
import json
import pytest

from iliad_payment import PaymentStatus
from .TestHelper import TestHelper


class TestPaymentStatus(TestHelper):
    def test_authorize(self):
        assert PaymentStatus.AUTHORIZE == 'authorize'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(AUTHORIZE\)',
        ):
            PaymentStatus.AUTHORIZE = self.random_string(10)

    def test_authorized(self):
        assert PaymentStatus.AUTHORIZED == 'authorized'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(AUTHORIZED\)',
        ):
            PaymentStatus.AUTHORIZED = self.random_string(10)

    def test_canceled(self):
        assert PaymentStatus.CANCELED == 'canceled'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(CANCELED\)',
        ):
            PaymentStatus.CANCELED = self.random_string(10)

    def test_capture(self):
        assert PaymentStatus.CAPTURE == 'capture'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(CAPTURE\)',
        ):
            PaymentStatus.CAPTURE = self.random_string(10)

    def test_captured(self):
        assert PaymentStatus.CAPTURED == 'captured'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(CAPTURED\)',
        ):
            PaymentStatus.CAPTURED = self.random_string(10)

    def test_disputed(self):
        assert PaymentStatus.DISPUTED == 'disputed'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(DISPUTED\)',
        ):
            PaymentStatus.DISPUTED = self.random_string(10)

    def test_expired(self):
        assert PaymentStatus.EXPIRED == 'expired'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(EXPIRED\)',
        ):
            PaymentStatus.EXPIRED = self.random_string(10)

    def test_failed(self):
        assert PaymentStatus.FAILED == 'failed'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(FAILED\)',
        ):
            PaymentStatus.FAILED = self.random_string(10)

    def test_to_capture(self):
        assert PaymentStatus.TO_CAPTURE == 'to_capture'

        with pytest.raises(
            SyntaxError,
            match = r'You can not modify a constant \(TO_CAPTURE\)',
        ):
            PaymentStatus.TO_CAPTURE = self.random_string(10)
