"""Test dispute object"""

import pytest
import responses

from iliad_payment import Dispute
from iliad_payment import Payment
from iliad_payment.core import AbstractAmount
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestDispute(TestHelper):
    def test_class(self):
        assert issubclass(Dispute, AbstractAmount)
        assert issubclass(Dispute, AbstractObject)

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
