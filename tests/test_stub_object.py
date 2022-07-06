"""Test abstract object"""

import base64
from datetime import datetime
from datetime import timezone
from datetime import tzinfo
import json
import pytest
from pytz import timezone as tz
from random import choice
import requests
import responses

from stancer import Card
from stancer import Config
from stancer.exceptions import StancerValueError
from .stub.stub_object import StubObject
from .TestHelper import TestHelper


class TestStubObject(TestHelper):
    def test__dict__(self):
        obj = StubObject()

        params = {
            'id': self.random_string(29),
            'string1': self.random_string(10),
            'integer1': self.random_integer(10, 100),
            'card1': {
                'id': self.random_string(29),
                'number': choice(self.card_number_provider()),
            },
            'created': self.random_integer(1500000000, 1600000000),
        }

        obj.force_populated(True)
        obj.hydrate(**params)
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
        assert isinstance(result['created'], datetime)
        assert result['created'].timestamp() == params['created']

        assert 'card1' in result
        assert isinstance(result['card1'], Card)
        assert result['card1'] == card

    @responses.activate
    def test_created(self):
        obj = StubObject()
        config = Config()
        zone = 'Europe/Paris'
        date = self.random_integer(1500000000, 1600000000)

        params = {
            'created': date,
        }

        obj.hydrate(**params)

        assert isinstance(obj.created, datetime)
        assert obj.created.timestamp() == date
        assert obj.created.tzinfo is timezone.utc

        config.default_timezone = tz(zone)

        obj.hydrate(**params)

        assert isinstance(obj.created, datetime)
        assert obj.created.timestamp() == date
        assert isinstance(obj.created.tzinfo, tzinfo)
        assert obj.created.tzinfo.zone == zone

        obj = StubObject(self.random_string(29))
        params = {
            'created': self.random_integer(1500000000, 1600000000),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.created, datetime)
        assert obj.created.timestamp() == params['created']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_instance(self):
        empty = StubObject()

        assert isinstance(empty, StubObject)
        assert empty.id is None
        assert empty.__dict__ == {}

        uid = self.random_string(29)
        with_id = StubObject(uid)
        with_id.force_populated(True)  # Prevent tests errors

        assert isinstance(with_id, StubObject)
        assert with_id.id == uid
        assert with_id.__dict__ == {'id': uid}

        params = {
            'string1': self.random_string(10),
            'string2': None,
            'integer1': self.random_integer(10, 100),
            'card1': {
                'id': self.random_string(29),
                'number': '4242424242424242',
            },
            'created': 1546867615,
        }

        hydrated = StubObject()
        hydrated.hydrate(**params)

        assert isinstance(hydrated, StubObject)
        assert hydrated.id is None
        assert hydrated.string1 == params['string1']
        assert hydrated.string2 is None
        assert hydrated.integer1 == params['integer1']

        assert isinstance(hydrated.card1, Card)
        assert hydrated.card1.id == params['card1']['id']

        assert isinstance(hydrated.created, datetime)
        assert hydrated.created.timestamp() == params['created']

        with_kwargs = StubObject(**params)

        assert isinstance(with_kwargs, StubObject)
        assert with_kwargs.id is None
        assert with_kwargs.string1 == params['string1']
        assert with_kwargs.string2 is None
        assert with_kwargs.integer1 == params['integer1']

        assert isinstance(with_kwargs.card1, Card)
        assert with_kwargs.card1.id == params['card1']['id']

        assert isinstance(with_kwargs.created, datetime)
        assert with_kwargs.created.timestamp() == params['created']

    @responses.activate
    def test_delete(self):
        obj = StubObject(self.random_string(29))

        responses.add(responses.DELETE, obj.uri, status=204)

        assert obj.delete() == obj
        assert len(responses.calls) == 1
        assert obj.id is None
        assert obj.is_modified

    def test_id(self):
        assert StubObject().id is None

        uid = self.random_string(29)
        obj = StubObject(uid)

        assert obj.id == uid

        with pytest.raises(AttributeError):
            obj.id = self.random_string(29)

    def test_hydrate(self):
        obj = StubObject()
        config = Config()
        uid = self.random_string(29)

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10, 100),
            'card1': {},
            'created': 1546867615,
        }

        assert obj.hydrate(**params) == obj

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']

        assert isinstance(obj.created, datetime)
        assert obj.created.tzinfo is timezone.utc
        assert obj.created.year == 2019
        assert obj.created.month == 1
        assert obj.created.day == 7
        assert obj.created.hour == 13
        assert obj.created.minute == 26
        assert obj.created.second == 55

        assert obj.card1 is None

        assert obj.is_modified

        assert obj.hydrate(card1=uid) == obj

        assert isinstance(obj.card1, Card)
        assert obj.card1.id == uid

        card = obj.card1

        params = {
            'card1': {
                'id': self.random_string(29),
            },
        }

        obj = StubObject()
        obj.hydrate(**params)

        assert isinstance(obj.card1, Card)
        assert obj.card1 != card
        assert obj.card1.id == params['card1']['id']

        assert obj.is_not_modified
        assert card.is_not_modified

        params = {
            'card1': card,
        }

        obj = StubObject()
        obj.hydrate(**params)

        assert isinstance(obj.card1, Card)
        assert obj.card1 == card

        assert obj.is_not_modified
        assert card.is_not_modified

        uid = self.random_string(29)
        name1 = self.random_string(10)
        name2 = self.random_string(10)

        params = {
            'cards': [
                card,
                {
                    'id': uid,
                    'name': name1,
                },
            ],
        }

        obj = StubObject()
        obj.hydrate(**params)

        assert isinstance(obj.cards, list)
        assert len(obj.cards) == 2

        assert isinstance(obj.cards[0], Card)
        assert obj.cards[0] == card

        assert isinstance(obj.cards[1], Card)
        assert obj.cards[1].id == uid
        assert obj.cards[1].name == name1

        assert obj.is_modified
        assert obj.cards[0].is_not_modified
        assert obj.cards[1].is_modified

        card0 = obj.cards[0]
        card1 = obj.cards[1]

        params = {
            'cards': [
                {
                    'id': uid,
                    'name': name2,
                },
            ],
        }

        obj.hydrate(**params)

        assert isinstance(obj.cards, list)
        assert len(obj.cards) == 2

        assert isinstance(obj.cards[0], Card)
        assert obj.cards[0] == card0

        assert isinstance(obj.cards[1], Card)
        assert obj.cards[1] == card1
        assert obj.cards[1].name == name2

        assert obj.is_modified
        assert obj.cards[0].is_not_modified
        assert obj.cards[1].is_modified

    @responses.activate
    def test_live_mode(self):
        obj = StubObject()

        assert obj.live_mode is None

        with pytest.raises(AttributeError):
            obj.live_mode = True

        obj = StubObject(self.random_string(29))
        params = {
            'live_mode': True,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.live_mode is True
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_modified_status(self):
        obj = StubObject()

        assert not obj.is_modified
        assert obj.is_not_modified

        obj.force_modified('id')

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
            'integer1': self.random_integer(10, 100),
            'card1': {
                'number': '4242424242424242',
            },
            'created': 1546867615,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.is_not_populated

        obj.force_modified('id')

        assert obj.is_modified

        obj.populate()

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']

        assert len(responses.calls) == 1
        assert obj.is_populated
        assert obj.card1.is_populated  # Inner object are populated too
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
            'integer1': self.random_integer(10, 100),
            'created': 1546867615,
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.string1 == params['string1']
        assert obj.integer1 == params['integer1']
        assert len(responses.calls) == 1

    @responses.activate
    def test_send(self):
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
            'integer1': self.random_integer(10, 100),
            'card1': {
                'number': '4242424242424242',
                'brand': self.random_string(10),
            },
            'created': 1546867615,
        }

        obj.hydrate(**params)
        obj.string2 = self.random_string(20)
        card = obj.card1

        uid = self.random_string(29)

        location = obj.uri
        obj_repr = obj.to_json()

        responses.add(responses.POST, location, json={'id': uid})

        assert obj.send() == obj
        assert obj.id == uid

        assert len(responses.calls) == 1
        assert 'Authorization' in responses.calls[0].request.headers
        assert responses.calls[0].request.headers['Authorization'] == theader
        assert responses.calls[0].request.body == obj_repr

        # Multiple send will not trigger multiple call
        obj.send()

        assert len(responses.calls) == 1

        conf.mode = Config.LIVE_MODE

        responses.add(responses.PATCH, location + '/' + uid, json={'id': uid})

        # Modified object allows new calls
        obj.string2 = self.random_string(20)
        obj_repr = obj.to_json()

        obj.send()

        assert len(responses.calls) == 2
        assert responses.calls[1].request.body == obj_repr

        # Change mode will change used key
        assert responses.calls[1].request.headers['Authorization'] == pheader

    def test_to_json(self):
        obj = StubObject()

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10, 100),
            'card1': {
                'brand': self.random_string(10),
                'number': '4242424242424242',
            },
            'created': 1546867615,
        }

        obj.hydrate(**params)
        card1 = obj.card1

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"string1":"{}"'.format(params['string1'])) > 0
        assert result.find('"integer1":{}'.format(params['integer1'])) > 0
        assert result.find('"card1":{{"number":"{}"}}'.format(card1.number)) > 0
        assert result.find('"created"') == -1
        assert result.find('"card2"') == -1

        # Inner object may send their ID
        card2 = Card(self.random_string(29))
        obj.card2 = card2

        result = obj.to_json()

        assert result.find('"card2":"{}"'.format(card2.id)) > 0

        # Only export modified properties
        obj.reset_modified()
        del card1._modified  # Do not do this at home
        del card2._modified  # Do not do this at home

        result = obj.to_json()

        assert isinstance(result, str)
        assert result == '{}'

        # An object with an ID will return only his ID into the json
        uid = self.random_string(29)
        obj.hydrate(id=uid)

        result = obj.to_json()

        assert result == '"{}"'.format(uid)

        # Unless it was modified
        obj.string2 = self.random_string(20)

        result = obj.to_json()

        assert isinstance(result, str)

        result = json.loads(result)

        assert 'string2' in result
        assert result['string2'] == obj.string2

        assert 'integer1' not in result

        assert 'id' not in result
        assert 'created' not in result

        # Export modified inner object
        card2.cvc = str(self.random_integer(100, 999))

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"card1"') == -1
        assert result.find('"card2":{{"cvc":"{}"}}'.format(card2.cvc)) > 0

        # Do not export empty object
        obj.card2 = Card()

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"card1"') == -1
        assert result.find('"card2"') == -1
