"""Test auth object"""

import json

import pytest

from stancer.auth import Auth
from stancer.core.abstract_object import AbstractObject
from stancer.core.enum.version import Version
from stancer.exceptions import InvalidUrlError
from stancer.status.auth import AuthStatus

from .TestHelper import TestHelper


class TestAuth(TestHelper):
    def test_class(self):
        assert issubclass(Auth, AbstractObject)

    def test_redirect_url(self):
        auth = Auth()

        assert auth.redirect_url is None

        with pytest.raises(AttributeError):
            auth.redirect_url = f'https://{self.random_string(15)}'

        params = {
            'redirect_url': f'https://{self.random_string(50)}',
        }
        auth.hydrate(**params)

        assert auth.redirect_url == params['redirect_url']

    def test_return_url_v1(self):
        auth = Auth()
        self.conf.version = Version.API_V1
        return_url = f'https://{self.random_string(50)}'

        assert auth.return_url is None

        auth.return_url = return_url

        assert auth.return_url == return_url

        exported = auth.to_json()

        assert isinstance(exported, str)
        # As the api V2 only accept boolean, even thought we have a Auth object, our json will only be a bool.
        assert exported.find(f'"return_url":"{return_url}"') > 0

    def test_return_url_v2(self):
        auth = Auth()
        self.conf.version = Version.API_V2
        bad_url = f'http://{self.random_string(50)}'
        return_url = f'https://{self.random_string(50)}'

        with pytest.raises(InvalidUrlError):
            auth.return_url = bad_url

        assert auth.return_url is None

        auth.return_url = return_url

        assert auth.return_url == return_url

        exported = auth.to_json()

        assert isinstance(exported, str)
        result = json.loads(exported)
        # As the api V2 only accept boolean, even thought we have a Auth object, our json will only be a bool.
        assert result is True
        assert auth.to_json_repr() is True

    def test_status_v1(self):
        auth = Auth()
        self.conf.version = Version.API_V1
        assert auth.status == AuthStatus.REQUEST

        exported = auth.to_json()

        assert isinstance(exported, str)
        assert exported.find('status') > 0

        with pytest.raises(AttributeError):
            auth.status = self.random_string(10)

    def test_status_v2(self):
        auth = Auth()
        self.conf.version = Version.API_V2
        assert auth.status == AuthStatus.REQUEST

        exported = auth.to_json()

        assert isinstance(exported, str)
        assert auth.to_json_repr() is True

        result = json.loads(exported)
        assert result is True

        with pytest.raises(AttributeError):
            auth.status = self.random_string(10)
