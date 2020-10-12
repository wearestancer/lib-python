"""Test abstract object with search"""

from inspect import isgenerator
import responses
from time import time

from .stub.stub_search import StubSearch
from .TestHelper import TestHelper


class TestStubSearch(TestHelper):
    @responses.activate
    def test_list(self):
        obj = StubSearch()

        created = int(time()) - self.random_integer(1_000, 2_000)
        limit = self.random_integer(1, 100)
        start = self.random_integer(0, 100_000)
        foo = self.random_string(10)

        with open('./tests/fixtures/stub/list.json') as opened_file:
            responses.add(responses.GET, obj.uri, body=opened_file.read())

        results = StubSearch.list(created=created, limit=limit, start=start, foo=foo)

        assert isgenerator(results)
        assert len(responses.calls) == 0

        item = next(results)

        assert isinstance(item, StubSearch)
        assert item.id == 'stub_JnU7xyTGJvxRWZuxvj78qz7e'

        assert len(responses.calls) == 1

        api_call = responses.calls[0]

        assert api_call.request.method == 'GET'
        assert api_call.request.body is None

        assert api_call.request.url.startswith(obj.uri)
        assert 'created={}'.format(created) in api_call.request.url
        assert 'limit={}'.format(limit) in api_call.request.url
        assert 'start={}'.format(start) in api_call.request.url
        assert 'foo' not in api_call.request.url

        item = next(results)

        assert isinstance(item, StubSearch)
        assert item.id == 'stub_p5tjCrXHy93xtVtVqvEJoC1c'

        assert len(responses.calls) == 1

        item = next(results)

        assert isinstance(item, StubSearch)
        assert item.id == 'stub_JnU7xyTGJvxRWZuxvj78qz7e'

        assert len(responses.calls) == 2

        api_call = responses.calls[1]

        assert api_call.request.method == 'GET'
        assert api_call.request.body is None

        assert api_call.request.url.startswith(obj.uri)
        assert 'created={}'.format(created) in api_call.request.url
        assert 'limit={}'.format(limit) in api_call.request.url
        assert 'start={}'.format(2) in api_call.request.url  # 2 => start + limit in response
        assert 'foo' not in api_call.request.url
