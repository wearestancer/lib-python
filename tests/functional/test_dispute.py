"""Functional tests for payment object"""

import json

from datetime import datetime
from datetime import timezone

import pytest

from stancer.dispute import Dispute
from stancer.payment import Payment

from .FunctionalTestHelper import FunctionalTestHelper


class TestFunctionalDispute(FunctionalTestHelper):
    @pytest.mark.future
    def test_list(self):
        """Testing V2 lists imply some workaround:
        Either adding an until to our listing, or an asc/desc param
        """
        index = 0
        with open(
            f'./tests/fixtures/disputes/expected-disputes-v{self.conf.version}.json',
            encoding='utf8',
        ) as opened_file:
            content = json.load(opened_file)
        expected = content['disputes']
        for dispute in Dispute.list(created=datetime(2025, 9, 24, 14, 44, 3), limit=10):
            assert isinstance(dispute, Dispute)

            assert dispute.amount == expected[index]['amount']
            assert dispute.id == expected[index]['id']
            assert dispute.response == expected[index]['response']

            assert isinstance(dispute.created, datetime)
            assert dispute.created == datetime.fromtimestamp(
                expected[index]['created'], timezone.utc
            )

            assert isinstance(dispute.payment, Payment)
            assert dispute.payment.id == expected[index]['payment']

            index += 1

            if index not in expected:
                break
