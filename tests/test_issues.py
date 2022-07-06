
import json
import responses

from stancer import Payment
from stancer import PaymentStatus
from .TestHelper import TestHelper


class TestIssues(TestHelper):
    @responses.activate
    def test_issue_1(self):
        payment = Payment('paym_rLFNuoBpTZuA2NaIx2XxPXrL')

        with open('./tests/fixtures/issue/1.json') as opened_file:
            content = json.load(opened_file)
        status = self.random_string(10)

        responses.add(responses.GET, payment.uri, json=content)
        responses.add(responses.PATCH, payment.uri, json={'status': status})

        assert payment.status == PaymentStatus.AUTHORIZED

        payment.status = PaymentStatus.CAPTURE

        assert payment.send() == payment
        assert payment.status == status

        body = json.loads(responses.calls[1].request.body)

        assert body.get('status') == PaymentStatus.CAPTURE
