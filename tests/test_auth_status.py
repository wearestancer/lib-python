"""Test auth status object"""

from datetime import date
import json
import pytest

from iliad_payment import AuthStatus
from .TestHelper import TestHelper


class TestAuthStatus(TestHelper):
    def test_attempted(self):
        assert AuthStatus.ATTEMPTED == 'attempted'

    def test_available(self):
        assert AuthStatus.AVAILABLE == 'available'

    def test_declined(self):
        assert AuthStatus.DECLINED == 'declined'

    def test_expired(self):
        assert AuthStatus.EXPIRED == 'expired'

    def test_failed(self):
        assert AuthStatus.FAILED == 'failed'

    def test_request(self):
        assert AuthStatus.REQUEST == 'request'

    def test_requested(self):
        assert AuthStatus.REQUESTED == 'requested'

    def test_success(self):
        assert AuthStatus.SUCCESS == 'success'

    def test_unavailable(self):
        assert AuthStatus.UNAVAILABLE == 'unavailable'
