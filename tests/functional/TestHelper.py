# -*- coding: utf-8 -*-

import os
import pytest
import random

from stancer import Config
from ..TestHelper import TestHelper as Helper


@pytest.mark.skipif(
    os.getenv('API_KEY') is None,
    reason='Require an API key',
)
@pytest.mark.skipif(
    os.getenv('API_HOST') is None,
    reason='Require an API host',
)
class TestHelper(Helper):
    def setup_method(self, method):
        conf = Config()

        del conf.keys
        conf.keys = str(os.getenv('API_KEY'))
        conf.host = str(os.getenv('API_HOST'))
        conf.timeout = 1

    def get_disputed_card_number(self):
        cards = [
            '4000000000000259',
            '4000000000001976',
            '4000000000005423',
        ]

        return random.choice(cards)

    def get_card_number(self):
        cards = [
            '4242424242424242',
            '5555555555554444',
            '4000000760000002',
            '4000001240000000',
            '4000004840000008',
            '4000000400000008',
            '4000000560000004',
            '4000002080000001',
            '4000002460000001',
            '4000002500000003',
            '4000002760000016',
            '4000003720000005',
            '4000003800000008',
            '4000004420000006',
            '4000005280000002',
            '4000005780000007',
            '4000006200000007',
            '4000006430000009',
            '4000007240000007',
            '4000007520000008',
            '4000007560000009',
            '4000008260000000',
            '4000000360000006',
            '4000001560000002',
            '4000003440000004',
            '4000003920000003',
            '3530111333300000',
            '4000005540000008',
            '4000007020000003',
        ]

        return random.choice(cards)
