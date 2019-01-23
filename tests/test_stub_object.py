"""Test core object"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

from builtins import *  # pylint: disable=unused-wildcard-import, wildcard-import
import base64
from datetime import datetime
import json
import pytest
import requests
import responses

from iliad_payment import Card
from iliad_payment import Config
from iliad_payment.exceptions import IliadValueError
from .stub.stub_object import StubObject
from .TestHelper import TestHelper


class TestStubObject(TestHelper):
    def test__dict__(self):
        obj = StubObject()

        params = {
            'id': self.random_string(29),
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': {
                'id': self.random_string(29),
                'number': '4242424242424242',
            },
            'created': 1546867615,
        }

        obj.force_populated(True)
        obj.hydrate(params)
        card = obj.card1

        result = obj.__dict__

        assert isinstance(result, dict)

        assert 'id' in result
        assert result['id'] == params['id']

        assert 'string1' in result
        assert result['string1'] == params['string1']

        assert 'integer1' in result
        assert result['integer1'] == params['integer1']

        assert 'created' in result
        assert result['created'] == '2019-01-07 14:26:55'

        assert 'card1' in result
        assert isinstance(result['card1'], dict)

        assert 'id' in result['card1']
        assert result['card1']['id'] == card.id

        assert 'number' in result['card1']
        assert result['card1']['number'] == card.number

    @responses.activate
    def test_delete(self):
        obj = StubObject()

        with pytest.raises(
            IliadValueError,
            match='You can not delete an object without an ID.',
        ):
            obj.delete()

        assert len(responses.calls) == 0

        obj = StubObject(self.random_string(29))

        responses.add(responses.DELETE, obj.uri, status=204)

        assert obj.delete() == obj
        assert len(responses.calls) == 1
        assert obj.id is None

    def test_id(self):
        assert StubObject().id is None

        uid = self.random_string(29)
        obj = StubObject(uid)

        assert obj.id == uid

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_hydrate(self):
        obj = StubObject()
        uid = self.random_string(29)

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': {},
            'created': 1546867615,
        }

        assert obj.hydrate(params) == obj

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']

        assert isinstance(obj.created, datetime)
        assert obj.created.year == 2019
        assert obj.created.month == 1
        assert obj.created.day == 7
        assert obj.created.hour == 14
        assert obj.created.minute == 26
        assert obj.created.second == 55

        assert isinstance(obj.card1, Card)
        assert obj.card1.id is None

        card = obj.card1

        assert obj.hydrate({'card1': uid}) == obj

        assert obj.card1 == card
        assert card.id == uid

        params = {
            'card1': {
                'id': self.random_string(29),
            },
        }

        obj = StubObject()
        obj.hydrate(params)

        assert isinstance(obj.card1, Card)
        assert obj.card1 != card
        assert obj.card1.id == params['card1']['id']

    def test_modified_status(self):
        obj = StubObject()

        assert not obj.is_modified
        assert obj.is_not_modified

        obj.force_modified(True)

        assert obj.is_modified

        # useless way to right it, please don't use it that way
        assert not obj.is_not_modified

    def test_populated_status(self):
        obj = StubObject()

        assert not obj.is_populated
        assert obj.is_not_populated

        obj.force_populated(True)

        assert obj.is_populated

        # useless way to right it, please don't use it that way
        assert not obj.is_not_populated

    @responses.activate
    def test_populate(self):
        obj = StubObject(self.random_string(29))

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'created': 1546867615,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.is_not_populated

        obj.force_modified(True)

        assert obj.is_modified

        obj.populate()

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']

        assert len(responses.calls) == 1
        assert obj.is_populated
        assert obj.is_not_modified

        # Multiple populate will not trigger multiple call
        obj.populate()

        assert len(responses.calls) == 1

        # No ID == no call
        StubObject().populate()

        assert len(responses.calls) == 1

    @responses.activate
    def test_populate_auto(self):
        obj = StubObject(self.random_string(29))
        conf = Config()

        conf.keys = 'stest_' + self.random_string(24)

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'created': 1546867615,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']
        assert len(responses.calls) == 1

    @responses.activate
    def test_save(self):
        obj = StubObject()
        conf = Config()

        stest = 'stest_' + self.random_string(24)
        sprod = 'sprod_' + self.random_string(24)

        phead = base64.b64encode((sprod + ':').encode())
        pheader = 'Basic {}'.format(phead.decode())

        thead = base64.b64encode((stest + ':').encode())
        theader = 'Basic {}'.format(thead.decode())

        conf.keys = (sprod, stest)

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': {
                'number': '4242424242424242',
                'brand': self.random_string(10),
            },
            'created': 1546867615,
        }

        obj.hydrate(params)
        obj.string2 = self.random_string(20)
        card = obj.card1

        uid = self.random_string(29)

        location = obj.uri
        obj_repr = obj.to_json()

        responses.add(responses.POST, location, json={'id': uid})

        assert obj.save() == obj
        assert obj.id == uid

        assert len(responses.calls) == 1
        assert 'Authorization' in responses.calls[0].request.headers
        assert responses.calls[0].request.headers['Authorization'] == theader
        assert responses.calls[0].request.body == obj_repr

        # Multiple save will not trigger multiple call
        obj.save()

        assert len(responses.calls) == 1

        conf.mode = Config.LIVE_MODE

        responses.add(responses.PATCH, location + '/' + uid, json={'id': uid})

        # Modified object allows new calls
        obj.string2 = self.random_string(20)
        obj_repr = obj.to_json()

        obj.save()

        assert len(responses.calls) == 2
        assert responses.calls[1].request.body == obj_repr

        # Change mode will change used key
        assert responses.calls[1].request.headers['Authorization'] == pheader

    def test_to_json(self):
        obj = StubObject()

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10),
            'card1': {
                'number': '4242424242424242',
                'brand': self.random_string(10),
            },
            'created': 1546867615,
        }

        obj.hydrate(params)
        card = obj.card1

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"string1":"{}"'.format(params['string1'])) > 0
        assert result.find('"integer1":{}'.format(params['integer1'])) > 0
        assert result.find('"card1":{{"number":"{}"}}'.format(card.number)) > 0
        assert result.find('"created"') == -1

        card.hydrate({'id': self.random_string(29)})

        result = obj.to_json()

        assert result.find('"card1":{{"id":"{}"}}'.format(card.id)) > 0

        # An object with an ID will return only his ID into the json
        uid = self.random_string(29)
        obj.hydrate({'id': uid})

        result = obj.to_json()

        assert result == '{{"id":"{}"}}'.format(uid)

        # unless it was modified
        obj.string2 = self.random_string(20)

        result = obj.to_json()

        assert isinstance(result, str)

        result = json.loads(result)

        assert 'string1' in result
        assert result['string1'] == obj.string1

        assert 'string2' in result
        assert result['string2'] == obj.string2

        assert 'integer1' in result
        assert result['integer1'] == obj.integer1

        assert 'card1' in result
        assert 'id' in result['card1']
        assert result['card1']['id'] == card.id

        assert 'id' not in result
        assert 'created' not in result
