"""Functional tests for payment object"""

from datetime import datetime
from datetime import timezone

from stancer import Dispute
from stancer import Payment
from .TestHelper import TestHelper


class TestFunctionalDispute(TestHelper):
    def test_list(self):
        index = 0
        expected = [
            {
                'amount': 5910,
                'created': datetime(2022, 2, 9, 20, 27, 36, tzinfo=timezone.utc),
                'currency': 'gbp',
                'id': 'dspt_C7GepinCuJ59jAnpU5sEQNgq',
                'payment': 'paym_ntUYpo7EZhAhBO6lsqgTdtNW',
                'response': '45',
            },
            {
                'amount': 7760,
                'created': datetime(2022, 2, 9, 20, 29, 28, tzinfo=timezone.utc),
                'currency': 'gbp',
                'id': 'dspt_hz4w3NNkoMAKDZiTxxK4hOR3',
                'payment': 'paym_GKlvNIXN4OChVodjTN1FRQq1',
                'response': '45',
            },
            {
                'amount': 9604,
                'created': datetime(2022, 2, 9, 20, 31, 4, tzinfo=timezone.utc),
                'currency': 'usd',
                'id': 'dspt_YPZ0oPcFrKOjCHtHZ1BqLK59',
                'payment': 'paym_MagWutVCvDU7JYjg8Rm2tLdb',
                'response': '45',
            },
            {
                'amount': 8383,
                'created': datetime(2022, 2, 9, 20, 32, 42, tzinfo=timezone.utc),
                'currency': 'gbp',
                'id': 'dspt_9zjvKu5JWjVHte09EeZRodnu',
                'payment': 'paym_wRS7Dh57F10c2vjVu8mxx1p3',
                'response': '45',
            },
            {
                'amount': 8603,
                'created': datetime(2022, 2, 9, 20, 32, 55, tzinfo=timezone.utc),
                'currency': 'usd',
                'id': 'dspt_Xsz7ZpvETt1526x8wQTx8trp',
                'payment': 'paym_QSDLEHV7vPbCJrFUgsY0A8LS',
                'response': '45',
            },
            {
                'amount': 1912,
                'created': datetime(2022, 2, 9, 20, 34, 57, tzinfo=timezone.utc),
                'currency': 'gbp',
                'id': 'dspt_WD2O1iOzmKtaceikbTDudin3',
                'payment': 'paym_MQQrmRP5roIEVS6QRfW7gwzz',
                'response': '45',
            }
        ]

        for dispute in Dispute.list(created=datetime(2022, 2, 9), limit=10):
            assert isinstance(dispute, Dispute)

            assert dispute.amount == expected[index]['amount']
            assert dispute.id == expected[index]['id']
            assert dispute.response == expected[index]['response']

            assert isinstance(dispute.created, datetime)
            assert dispute.created == expected[index]['created']

            assert isinstance(dispute.payment, Payment)
            assert dispute.payment.id == expected[index]['payment']

            index += 1

            if index not in expected:
                break
