"""Test auth object"""

import pytest
import responses

from iliad_payment import Auth
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestAuth(TestHelper):
    def test_class(self):
        assert issubclass(Auth, AbstractObject)

        attrs = Auth._get_allowed_attributes()

        assert isinstance(attrs, list)

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
