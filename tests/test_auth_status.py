"""Test auth status object"""

from stancer import AuthStatus
from .TestHelper import TestHelper


class TestAuthStatus(TestHelper):
    def test_attempted(self):
        assert AuthStatus.ATTEMPTED == 'attempted'
        assert AuthStatus.has_member('ATTEMPTED')
        assert AuthStatus.has_value('attempted')

    def test_available(self):
        assert AuthStatus.AVAILABLE == 'available'
        assert AuthStatus.has_member('AVAILABLE')
        assert AuthStatus.has_value('available')

    def test_declined(self):
        assert AuthStatus.DECLINED == 'declined'
        assert AuthStatus.has_member('DECLINED')
        assert AuthStatus.has_value('declined')

    def test_expired(self):
        assert AuthStatus.EXPIRED == 'expired'
        assert AuthStatus.has_member('EXPIRED')
        assert AuthStatus.has_value('expired')

    def test_failed(self):
        assert AuthStatus.FAILED == 'failed'
        assert AuthStatus.has_member('FAILED')
        assert AuthStatus.has_value('failed')

    def test_request(self):
        assert AuthStatus.REQUEST == 'request'
        assert AuthStatus.has_member('REQUEST')
        assert AuthStatus.has_value('request')

    def test_requested(self):
        assert AuthStatus.REQUESTED == 'requested'
        assert AuthStatus.has_member('REQUESTED')
        assert AuthStatus.has_value('requested')

    def test_success(self):
        assert AuthStatus.SUCCESS == 'success'
        assert AuthStatus.has_member('SUCCESS')
        assert AuthStatus.has_value('success')

    def test_unavailable(self):
        assert AuthStatus.UNAVAILABLE == 'unavailable'
        assert AuthStatus.has_member('UNAVAILABLE')
        assert AuthStatus.has_value('unavailable')
