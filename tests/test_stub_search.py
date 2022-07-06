"""Test abstract object with search"""

from inspect import isgenerator
import pytest
import responses
from time import time

from stancer.exceptions import InvalidSearchResponse

from .stub.stub_search import StubSearch
from .TestHelper import TestHelper


class TestStubSearch(TestHelper):
    @responses.activate
    def test_bad_response(self):
        obj = StubSearch()

        created = int(time()) - self.random_integer(1_000, 2_000)
        location = '{}?created={}'.format(obj.uri, created)

        responses.add(responses.GET, location, body='[')

        with pytest.raises(
            InvalidSearchResponse,
            match='Invalid results.',
        ):
            items = StubSearch.list(created=created)
            next(items)

        body = {
            'range': {
                'has_more': False,
                'limit': 10,
            },
        }

        responses.reset()
        responses.add(responses.GET, location, json=body)

        with pytest.raises(
            InvalidSearchResponse,
            match='Results not found.',
        ):
            items = StubSearch.list(created=created)
            next(items)

        body = {
            self.random_string(2): {},
            self.random_string(2): {},
        }

        responses.reset()
        responses.add(responses.GET, location, json=body)

        with pytest.raises(
            InvalidSearchResponse,
            match='Results not found.',
        ):
            items = StubSearch.list(created=created)
            next(items)

    @responses.activate
    def test_empty_list(self):
        obj = StubSearch()

        created = int(time()) - self.random_integer(1_000, 2_000)
        limit = self.random_integer(1, 100)
        start = self.random_integer(0, 100_000)

        responses.add(responses.GET, obj.uri, status=404)

        results = StubSearch.list(created=created, limit=limit, start=start)

        assert isgenerator(results)
        assert len(responses.calls) == 0

        for item in results:
            assert False  # Should not be trigger as we have no results

        assert len(responses.calls) == 1

        api_call = responses.calls[0]

        assert api_call.request.method == 'GET'
        assert api_call.request.body is None

        assert api_call.request.url.startswith(obj.uri)
        assert 'created={}'.format(created) in api_call.request.url
        assert 'limit={}'.format(limit) in api_call.request.url
        assert 'start={}'.format(start) in api_call.request.url

    @responses.activate
    def test_list(self):
        obj = StubSearch()

        created = int(time()) - self.random_integer(1_000, 2_000)
        limit = self.random_integer(1, 100)
        start = self.random_integer(0, 100_000)
        foo = self.random_string(10)
        foobar = self.random_string(10)

        with open('./tests/fixtures/stub/list.json') as opened_file:
            responses.add(responses.GET, obj.uri, body=opened_file.read())

        results = StubSearch.list(created=created, limit=limit, start=start, foo=foo, foobar=foobar)

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
        assert 'foo={}'.format(foo) in api_call.request.url
        assert 'foobar' not in api_call.request.url

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
        assert 'foo={}'.format(foo) in api_call.request.url
        assert 'foobar' not in api_call.request.url
