"""Test abstract object"""

from datetime import datetime
import json
from .stub.stub_with_default import StubWithDefault
from .TestHelper import TestHelper


class TestStubWithDefault(TestHelper):
    def test__dict__(self):
        obj = StubWithDefault()

        params = {
            'id': self.random_string(29),
            'string1': self.random_string(10),
            'integer1': self.random_integer(10, 100),
            'created': self.random_integer(1500000000, 1600000000),
        }

        obj.force_populated(True)
        obj.hydrate(**params)

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

    def test_instance(self):
        empty = StubWithDefault()
        expected = {
            'string1': 'Default value for string1',
        }

        assert isinstance(empty, StubWithDefault)
        assert empty.id is None
        assert empty.__dict__ == expected

        uid = self.random_string(29)
        with_id = StubWithDefault(uid)
        with_id.force_populated(True)  # Prevent tests errors

        assert isinstance(with_id, StubWithDefault)
        assert with_id.id == uid
        assert with_id.__dict__ == {'id': uid, **expected}

        params = {
            'string1': self.random_string(10),
            'string2': None,
            'integer1': self.random_integer(10, 100),
        }

        hydrated = StubWithDefault()
        hydrated.hydrate(**params)

        assert isinstance(hydrated, StubWithDefault)
        assert hydrated.id is None
        assert hydrated.string1 == params['string1']
        assert hydrated.string2 is None
        assert hydrated.integer1 == params['integer1']

        with_kwargs = StubWithDefault(**params)

        assert isinstance(with_kwargs, StubWithDefault)
        assert with_kwargs.id is None
        assert with_kwargs.string1 == params['string1']
        assert with_kwargs.string2 is None
        assert with_kwargs.integer1 == params['integer1']

    def test_to_json(self):
        obj = StubWithDefault()

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"string1":"Default value for string1"') > 0

        params = {
            'string1': self.random_string(10),
            'integer1': self.random_integer(10, 100),
            'created': 1546867615,
        }

        obj.hydrate(**params)

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"string1":"{}"'.format(params['string1'])) > 0
        assert result.find('"integer1":{}'.format(params['integer1'])) > 0
        assert result.find('"created"') == -1

        # Only export modified properties
        obj.reset_modified()

        result = obj.to_json()

        assert isinstance(result, str)
        assert result == '{}'

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
