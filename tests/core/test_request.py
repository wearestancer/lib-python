"""Test request object"""

import base64
import pytest
import responses

from stancer import Config
from stancer.core import Request
from stancer.exceptions import StancerValueError
from stancer.exceptions import UnauthorizedError
from ..stub.stub_object import StubObject
from ..TestHelper import TestHelper


class TestRequest(TestHelper):
    @responses.activate
    def test_unknown_method(self):
        obj = StubObject()
        req = Request()

        with pytest.raises(
            StancerValueError,
            match='Invalid HTTP method.',
        ):
            req._request(self.random_string(10), obj)

        assert len(responses.calls) == 0

    @responses.activate
    @pytest.mark.parametrize(
        'key, mode, prefix',
        TestHelper.secret_api_key_provider(),
    )
    def test_api_key_validation(self, key, mode, prefix):
        obj = StubObject(self.random_string(29))
        req = Request()
        conf = Config()

        previous_keys = conf.keys
        del conf.keys

        with pytest.raises(
            AttributeError,
            match='No API key found.',
        ):
            req.get(obj)

        assert len(responses.calls) == 0

        conf.mode = mode
        conf.keys = key

        # Bad key
        with open('./tests/fixtures/auth/not-authorized.json') as opened_file:
            content = opened_file.read()

        responses.add(responses.GET, obj.uri, body=content, status=401)

        with pytest.raises(UnauthorizedError) as error:
            req.get(obj)

        assert error.value.status_code == 401
        assert error.value.reason == 'Unauthorized'
        assert error.value.type == 'invalid_request_error'
        tmp = 'You are not authorized to access that resource'
        assert error.value.message == tmp

        assert len(responses.calls) == 1

        # All ok
        responses.reset()
        responses.add(responses.GET, obj.uri, json={})

        assert req.get(obj) == req
        assert len(responses.calls) == 1

        del conf.mode
        del conf.keys
        conf.keys = previous_keys

    @responses.activate
    @pytest.mark.parametrize(
        'key, mode, prefix',
        TestHelper.public_api_key_provider(),
    )
    def test_api_public_key_error(self, key, mode, prefix):
        obj = StubObject(self.random_string(29))
        req = Request()
        conf = Config()

        previous_keys = conf.keys
        del conf.keys

        with pytest.raises(
            AttributeError,
            match='No API key found.',
        ):
            req.get(obj)

        assert len(responses.calls) == 0

        conf.mode = mode
        conf.keys = key

        with pytest.raises(
            AttributeError,
            match='No API key found.',
        ):
            req.get(obj)

        assert len(responses.calls) == 0

        del conf.mode
        del conf.keys
        conf.keys = previous_keys

    @responses.activate
    @pytest.mark.parametrize(
        'status_code, cls',
        TestHelper.http_code_provider(),
    )
    def test_exceptions(self, status_code, cls):
        obj = StubObject(self.random_string(29))
        req = Request()

        responses.add(responses.GET, obj.uri, status=status_code)

        with pytest.raises(cls):
            req.get(obj)

        assert len(responses.calls) == 1

    @responses.activate
    def test_delete(self):
        obj = StubObject()
        req = Request()
        conf = Config()
        conf.mode = Config.TEST_MODE
        location = obj.uri

        responses.add(responses.DELETE, obj.uri, status=204)

        assert req.delete(obj) == req
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
        req = Request()
        conf = Config()
        conf.mode = Config.TEST_MODE

        responses.add(responses.GET, obj.uri, json={})

        assert req.get(obj) == req
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

        # Call without update and query params
        responses.reset()

        body = self.random_string(10)
        key = self.random_string(5)
        value = self.random_string(5)
        params = {
            key: value,
        }

        responses.add(responses.GET, obj.uri, body=body)

        resp = req.get(obj, update=False, **params)

        assert isinstance(resp, str)
        assert resp == body

        api_call = responses.calls[0]

        assert api_call.request.method == 'GET'
        assert api_call.request.url == '{}?{}={}'.format(obj.uri, key, value)
        assert api_call.request.body is None

    @responses.activate
    def test_patch(self):
        obj = StubObject()
        req = Request()
        conf = Config()
        conf.mode = Config.TEST_MODE

        obj.hydrate(string1=self.random_string(10, 20), integer1=self.random_integer(10, 999999))

        ret = {
            'id': self.random_string(29),
        }

        obj.reset_modified()

        responses.add(responses.PATCH, obj.uri, json=ret)

        location = obj.uri
        body = obj.to_json()

        assert req.patch(obj) == req
        assert obj.id == ret['id']
        assert len(responses.calls) == 1

        tmp = base64.b64encode((conf.stest + ':').encode())
        auth = 'Basic {}'.format(tmp.decode())

        api_call = responses.calls[0]

        assert api_call.request.method == 'PATCH'
        assert api_call.request.url == location
        assert api_call.request.body == body

        assert 'Authorization' in api_call.request.headers
        assert api_call.request.headers['Authorization'] == auth

        assert 'Content-Type' in api_call.request.headers
        assert api_call.request.headers['Content-Type'] == 'application/json'

    @responses.activate
    def test_post(self):
        obj = StubObject()
        req = Request()
        conf = Config()
        conf.mode = Config.TEST_MODE

        obj.hydrate(string1=self.random_string(10, 20), integer1=self.random_integer(10, 999999))

        ret = {
            'id': self.random_string(29),
        }

        obj.reset_modified()

        responses.add(responses.POST, obj.uri, json=ret)

        location = obj.uri
        body = obj.to_json()

        assert req.post(obj) == req
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
