"""Test auth object"""

import pytest
import responses

from iliad_payment import Auth
from iliad_payment import AuthStatus
from iliad_payment.core import AbstractObject
from iliad_payment.exceptions import InvalidUrlError
from .TestHelper import TestHelper


class TestAuth(TestHelper):
    def test_class(self):
        assert issubclass(Auth, AbstractObject)

    @responses.activate
    def test_redirect_url(self):
        obj = Auth()

        assert obj.redirect_url is None

        with pytest.raises(AttributeError):
            obj.redirect_url = 'https://' + self.random_string(15)

        obj = Auth(self.random_string(29))
        params = {
            'redirect_url': 'https://' + self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.redirect_url == params['redirect_url']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
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

        with pytest.raises(InvalidUrlError):
            obj.return_url = bad_url

        obj = Auth(self.random_string(29))
        params = {
            'return_url': 'https://' + self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.return_url == params['return_url']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_status(self):
        obj = Auth()

        assert obj.status == AuthStatus.REQUEST

        exported = obj.to_json()

        assert isinstance(exported, str)
        assert exported.find('"status":"{}"'.format(AuthStatus.REQUEST)) > 0

        with pytest.raises(AttributeError):
            obj.status = self.random_string(10)
