# -*- coding: utf-8 -*-

import os
import random

import pytest

from stancer import Config
from stancer.core.enum import Version

from ..TestHelper import TestHelper


@pytest.mark.skipif(
    os.getenv('API_KEY') is None,
    reason='Require an API key',
)
@pytest.mark.skipif(
    os.getenv('API_HOST') is None,
    reason='Require an API host',
)
class FunctionalTestHelper(TestHelper):
    def setup_method(self, method):
        self.conf = Config()
        del self.conf.keys
        self.conf.keys = str(os.getenv('API_KEY'))
        self.conf.host = str(os.getenv('API_HOST'))
        self.conf.timeout = 5
        version_param = os.getenv('API_VERSION')
        self.conf.version = version_param if version_param else Version.API_V1

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
            # '4000000760000002', This card emulates fictionless do not use for auth testing
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
            # '4000005780000007', This card as a probleme with there country
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
            # '4000005540000008', # This card create a lot of refused auth
            '4000007020000003',
        ]

        return random.choice(cards)

    def get_not_found_message(self, tested_object):
        name = str(tested_object.__class__.__name__)
        return (
            f'No such {name.lower()} {format(tested_object.id)}'
            if self.conf.version == Version.API_V1 else
            f'{name.capitalize()} `{format(tested_object.id)}` not found')
