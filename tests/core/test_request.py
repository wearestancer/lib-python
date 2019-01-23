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
from iliad_payment.exceptions import IliadValueError
from iliad_payment.exceptions import NotAuthorizedError
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
        obj = StubObject(self.random_string(29))
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

        # Bad key
        with open('./tests/fixtures/auth/not-authorized.json') as opened_file:
            content = opened_file.read()

        responses.add(responses.GET, obj.uri, body=content, status=401)

        with pytest.raises(NotAuthorizedError) as error:
            req.get

            assert error.status_code == 401
            assert error.reason == 'Not Authorized'
            assert error.type == 'invalid_request_error'
            tmp = 'You are not authorized to access that resource'
            assert error.message == tmp

            assert len(responses.calls) == 1

        # All ok
        responses.reset()
        responses.add(responses.GET, obj.uri, json={})

        assert req.get == req
        assert len(responses.calls) == 1

        del conf.mode
        del conf.keys
        conf.keys = previous_keys

    @responses.activate
    @pytest.mark.parametrize('status_code, cls', TestHelper.http_code_provider())
    def test_exceptions(self, status_code, cls):
        obj = StubObject(self.random_string(29))
        req = Request(obj)

        responses.add(responses.GET, obj.uri, status=status_code)

        with pytest.raises(cls):
            req.get

            assert len(responses.calls) == 1

    @responses.activate
    def test_delete(self):
        obj = StubObject()
        req = Request(obj)
        conf = Config()
        conf.mode = Config.TEST_MODE

        with pytest.raises(
            IliadValueError,
            match='You can not delete an object without an ID.',
        ):
            req.delete

        assert len(responses.calls) == 0

        obj = StubObject(self.random_string(29))
        req = Request(obj)
        location = obj.uri

        responses.add(responses.DELETE, obj.uri, status=204)

        assert req.delete == req
        assert len(responses.calls) == 1

        tmp = base64.b64encode((conf.stest + ':').encode())
        auth = 'Basic {}'.format(tmp.decode())

        api_call = responses.calls[0]

        assert obj.id is None

        assert api_call.request.method == 'DELETE'
        assert api_call.request.url == location
        assert api_call.request.body is None

        assert 'Authorization' in api_call.request.headers
        assert api_call.request.headers['Authorization'] == auth

        assert 'Content-Type' in api_call.request.headers
        assert api_call.request.headers['Content-Type'] == 'application/json'

    @responses.activate
    def test_get(self):
        obj = StubObject()
        req = Request(obj)
        conf = Config()
        conf.mode = Config.TEST_MODE

        with pytest.raises(
            IliadValueError,
            match='You can not get an object without an ID.',
        ):
            req.get

        assert len(responses.calls) == 0

        obj = StubObject(self.random_string(29))
        req = Request(obj)

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
