"""Test dispute object"""

import pytest
import responses

from stancer import Dispute
from stancer import Payment
from stancer.core import AbstractAmount
from stancer.core import AbstractObject
from stancer.core import AbstractSearch
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
