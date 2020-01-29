"""Test refund object"""

import pytest
import responses

from iliad_payment import Payment
from iliad_payment import Refund
from iliad_payment.core import AbstractAmount
from iliad_payment.core import AbstractObject
from .TestHelper import TestHelper


class TestRefund(TestHelper):
    def test_class(self):
        assert issubclass(Refund, AbstractAmount)
        assert issubclass(Refund, AbstractObject)

        assert Refund._ENDPOINT == 'refunds'

    @responses.activate
    def test_payment(self):
        obj = Refund()
        payment = Payment()

        assert obj.payment is None

        with pytest.raises(AttributeError):
            obj.payment = payment

        obj = Refund(self.random_string(29))
        params = {
            'payment': self.random_string(50),
        }

        responses.add(responses.GET, obj.uri, json=params)

        assert isinstance(obj.payment, Payment)
        assert obj.payment.id == params['payment']
        assert obj.is_populated
        assert len(responses.calls) == 1

    def test_status(self):
        obj = Refund()

        assert obj.status is None

        with pytest.raises(AttributeError):
            obj.status = self.random_string(29)

        params = {
            'status': self.random_string(10),
        }

        obj.hydrate(**params)

        assert obj.status == params['status']
