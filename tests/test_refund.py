"""Test refund object"""

from datetime import datetime
from datetime import timezone
from datetime import tzinfo
import pytest
from pytz import timezone as tz
import responses

from stancer import Config
from stancer import Payment
from stancer import Refund
from stancer import RefundStatus
from stancer.core import AbstractAmount
from stancer.core import AbstractObject
from .TestHelper import TestHelper


class TestRefund(TestHelper):
    def test_class(self):
        assert issubclass(Refund, AbstractAmount)
        assert issubclass(Refund, AbstractObject)

        assert Refund._ENDPOINT == 'refunds'

    def test_date_bank(self):
        obj = Refund()
        config = Config()
        date = self.random_integer(1500000000, 1600000000)
        zone = self.random_timezone()

        assert obj.date_bank is None

        with pytest.raises(AttributeError):
            obj.date_bank = date

        params = {
            'date_bank': date,
        }

        obj.hydrate(**params)

        assert isinstance(obj.date_bank, datetime)
        assert obj.date_bank.timestamp() == date
        assert obj.date_bank.tzinfo is timezone.utc

        config.default_timezone = tz(zone)

        obj.hydrate(**params)

        assert isinstance(obj.date_bank, datetime)
        assert obj.date_bank.timestamp() == date
        assert isinstance(obj.date_bank.tzinfo, tzinfo)
        assert obj.date_bank.tzinfo.zone == zone

    def test_date_refund(self):
        obj = Refund()
        config = Config()
        date = self.random_integer(1500000000, 1600000000)
        zone = self.random_timezone()

        assert obj.date_refund is None

        with pytest.raises(AttributeError):
            obj.date_refund = date

        params = {
            'date_refund': date,
        }

        obj.hydrate(**params)

        assert isinstance(obj.date_refund, datetime)
        assert obj.date_refund.timestamp() == date
        assert obj.date_refund.tzinfo is timezone.utc

        config.default_timezone = tz(zone)

        obj.hydrate(**params)

        assert isinstance(obj.date_refund, datetime)
        assert obj.date_refund.timestamp() == date
        assert isinstance(obj.date_refund.tzinfo, tzinfo)
        assert obj.date_refund.tzinfo.zone == zone

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

        # Works with constants

        params = {
            'status': 'refunded',
        }

        obj.hydrate(**params)

        assert obj.status == params['status']
        assert obj.status == RefundStatus.REFUNDED

    def test_to_json(self):
        obj = Refund()
        payment = Payment(self.random_string(29))

        params = {
            'amount': self.random_integer(50, 9999999),
            'payment': payment,
        }

        obj.hydrate(**params)

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"amount":{}'.format(params['amount'])) > 0
        assert result.find('"payment":"{}"'.format(payment.id)) > 0

        obj = Refund()

        params = {
            'payment': payment,
        }

        obj.hydrate(**params)

        result = obj.to_json()

        assert isinstance(result, str)
        assert result.find('"amount":') == -1
        assert result.find('"payment":"{}"'.format(payment.id)) > 0
