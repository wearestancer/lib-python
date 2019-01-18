"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import base64
import pytest
import responses

from iliad_payment import Config
from iliad_payment.core import Request
from ..stub.stub_object import StubObject
from ..TestHelper import TestHelper


class TestRequest(TestHelper):
    @responses.activate
    def test_unknown_method(self):
        obj = StubObject()
        req = Request(obj)

        assert req.plop == req
        assert len(responses.calls) == 0

    @responses.activate
    @pytest.mark.parametrize('key, mode, prefix', TestHelper.api_key_provider())
    def test_api_key_validation(self, key, mode, prefix):
        obj = StubObject()
        req = Request(obj)
        conf = Config()

        previous_keys = conf.keys
        del conf.keys

        with pytest.raises(
            AttributeError,
            match='No API key found.',
        ):
            req.get

        assert len(responses.calls) == 0

        conf.mode = mode
        conf.keys = key

        responses.add(responses.GET, obj.uri, json={})

        assert req.get == req
        assert len(responses.calls) == 1

        del conf.mode
        del conf.keys
        conf.keys = previous_keys

    @responses.activate
    def test_get(self):
        obj = StubObject(self.random_string(29))
        req = Request(obj)
        conf = Config()
        conf.mode = Config.TEST_MODE

        responses.add(responses.GET, obj.uri, json={})

        assert req.get == req
        assert len(responses.calls) == 1

        tmp = base64.b64encode((conf.stest + ':').encode())
        auth = 'Basic {}'.format(tmp.decode())

        api_call = responses.calls[0]

        assert api_call.request.method == 'GET'
        assert api_call.request.url == obj.uri
        assert api_call.request.body is None

        assert 'Authorization' in api_call.request.headers
        assert api_call.request.headers['Authorization'] == auth

        assert 'Content-Type' in api_call.request.headers
        assert api_call.request.headers['Content-Type'] == 'application/json'

    @responses.activate
    def test_post(self):
        obj = StubObject()
        req = Request(obj)
        conf = Config()
        conf.mode = Config.TEST_MODE

        obj.hydrate({
            'string1': self.random_string(10, 20),
            'integer1': self.random_integer(10, 999999),
        })

        ret = {
            'id': self.random_string(29),
        }

        obj.force_modified(False)

        responses.add(responses.POST, obj.uri, json=ret)

        location = obj.uri
        body = obj.to_json()

        assert req.post == req
        assert obj.id == ret['id']
        assert len(responses.calls) == 1

        tmp = base64.b64encode((conf.stest + ':').encode())
        auth = 'Basic {}'.format(tmp.decode())

        api_call = responses.calls[0]

        assert api_call.request.method == 'POST'
        assert api_call.request.url == location
        assert api_call.request.body == body

        assert 'Authorization' in api_call.request.headers
        assert api_call.request.headers['Authorization'] == auth

        assert 'Content-Type' in api_call.request.headers
        assert api_call.request.headers['Content-Type'] == 'application/json'

        obj.force_modified(True)

        responses.add(responses.PATCH, obj.uri)

        location = obj.uri
        body = obj.to_json()

        assert req.post == req
        assert len(responses.calls) == 2

        api_call = responses.calls[1]

        assert api_call.request.method == 'PATCH'
        assert api_call.request.url == obj.uri
        assert api_call.request.body == body

        assert 'Authorization' in api_call.request.headers
        assert api_call.request.headers['Authorization'] == auth

        assert 'Content-Type' in api_call.request.headers
        assert api_call.request.headers['Content-Type'] == 'application/json'
