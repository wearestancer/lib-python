"""Test auth object"""

import pytest

from stancer import Auth
from stancer import AuthStatus
from stancer.core import AbstractObject
from .TestHelper import TestHelper


class TestAuth(TestHelper):
    def test_class(self):
        assert issubclass(Auth, AbstractObject)

    def test_redirect_url(self):
        obj = Auth()

        assert obj.redirect_url is None

        with pytest.raises(AttributeError):
            obj.redirect_url = 'https://' + self.random_string(15)

        params = {
            'redirect_url': 'https://' + self.random_string(50),
        }
        obj.hydrate(**params)

        assert obj.redirect_url == params['redirect_url']

    def test_return_url(self):
        obj = Auth()
        bad_url = 'http://' + self.random_string(50)
        return_url = 'https://' + self.random_string(50)

        assert obj.return_url is None

        obj.return_url = return_url

        assert obj.return_url == return_url

        exported = obj.to_json()

        assert isinstance(exported, str)
        assert exported.find('"return_url":"{}"'.format(return_url)) > 0

    def test_status(self):
        obj = Auth()

        assert obj.status == AuthStatus.REQUEST

        exported = obj.to_json()

        assert isinstance(exported, str)
        assert exported.find('"status":"{}"'.format(AuthStatus.REQUEST)) > 0

        with pytest.raises(AttributeError):
            obj.status = self.random_string(10)
