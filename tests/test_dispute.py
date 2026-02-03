"""Test dispute object"""

import pytest
import responses

from stancer.core.abstract_amount import AbstractAmount
from stancer.core.abstract_object import AbstractObject
from stancer.core.abstract_search import AbstractSearch
from stancer.dispute import Dispute
from stancer.payment import Payment

from .TestHelper import TestHelper


class TestDispute(TestHelper):
    def test_class(self):
        assert issubclass(Dispute, AbstractAmount)
        assert issubclass(Dispute, AbstractObject)
        assert issubclass(Dispute, AbstractSearch)

    @responses.activate
    def test_order_id(self):
        obj = Dispute()

        assert obj.order_id is None

        with pytest.raises(AttributeError):
            obj.order_id = self.random_string(36)

        obj = Dispute(self.random_string(29))
        params = {
            'order_id': self.random_string(36),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.order_id == params['order_id']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_payment(self):
        obj = Dispute()
        payment = Payment()

        assert obj.payment is None

        with pytest.raises(AttributeError):
            obj.payment = payment

        obj = Dispute(self.random_string(29))
        params = {
            'payment': self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.payment, Payment)
        assert obj.payment.id == params['payment']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @responses.activate
    def test_response(self):
        obj = Dispute()

        assert obj.response is None

        with pytest.raises(AttributeError):
            obj.response = self.random_string(29)

        obj = Dispute(self.random_string(29))
        params = {
            'response': self.random_string(2),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert obj.response == params['response']
        assert obj.is_populated
        assert len(responses.calls) == 1

    @pytest.mark.parametrize('host', TestHelper.host_provider())
    @pytest.mark.parametrize('version', TestHelper.version_provider())
    def test_uri(self, host, version):
        self.conf.version = version
        self.conf.host = host
        obj = Dispute()
        uid = self.random_string(29)
        assert obj.uri == f'https://{host}/v{version}/disputes/'

        obj.hydrate(id=uid)

        assert obj.uri == f'https://{host}/v{version}/disputes/{uid}'

        with pytest.raises(AttributeError):
            obj.uri = self.random_string(29)
