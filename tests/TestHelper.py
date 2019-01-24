# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import date
import pytest
from random import randint, choice
import string

from iliad_payment import Config
from iliad_payment.exceptions import *  # pylint: disable=wildcard-import


class TestHelper(object):
    """Add some helper for tests."""

    def setup_method(self, method):
        conf = Config()

        conf.keys = 'stest_' + self.random_string(24)

    def random_integer(self, min, max=0):
        if max < min:
            (min, max) = (max, min)

        return randint(min, max)

    def random_string(self, min, max=None):
        chars = list(string.ascii_letters) + list(string.digits)

        if max is None:
            max = min

        if max < min:
            (min, max) = (max, min)

        limit = self.random_integer(min, max)

        return ''.join(choice(chars) for i in range(limit))

    def random_mobile(self):
        # Simulate a french mobile phone number
        first = self.random_integer(6, 7)
        counter = 4

        mobile = '+33' + str(first)

        if first == 7:
            mobile += str(self.random_integer(30, 99)).zfill(2)
            counter -= 1

        for idx in range(counter):
            mobile += str(self.random_integer(0, 99)).zfill(2)

        return mobile

    def random_year(self):
        return self.random_integer(0, 20) + self.current_year

    @property
    def current_year(self):
        return date.today().year

    @classmethod
    def api_key_provider(cls):
        obj = TestHelper()

        return [
            ('pprod_' + obj.random_string(24), Config.LIVE_MODE, 'pprod'),
            ('sprod_' + obj.random_string(24), Config.LIVE_MODE, 'sprod'),
            ('ptest_' + obj.random_string(24), Config.TEST_MODE, 'ptest'),
            ('stest_' + obj.random_string(24), Config.TEST_MODE, 'stest'),
        ]

    @classmethod
    def card_brand_provider(cls):
        obj = TestHelper()
        unknown_brand = obj.random_string(10)

        return [
            ('visa', 'VISA'),
            ('mastercard', 'MasterCard'),
            ('amex', 'American Express'),
            ('jcb', 'JCB'),
            ('maestro', 'Maestro'),
            ('discover', 'Discover'),
            ('dankort', 'Dankort'),
            (unknown_brand, unknown_brand),
        ]

    @classmethod
    def card_number_provider(cls):
        return (
            # VISA
            '4532160583905253',
            '4103344114503410',
            '4716929813250776300',

            # MasterCard
            '5312580044202748',
            '2720995588028031',
            '5217849688268117',

            # American Express (AMEX)
            '370301138747716',
            '340563568138644',
            '371461161518951',

            # Discover
            '6011651456571367',
            '6011170656779399',
            '6011693048292929421',

            # JCB
            '3532433013111566',
            '3544337258139297',
            '3535502591342895821',

            # Diners Club - North America
            '5480649643931654',
            '5519243149714783',
            '5509141180527803',

            # Diners Club - Carte Blanche
            '30267133988393',
            '30089013015810',
            '30109478108973',

            # Diners Club - International
            '36052879958170',
            '36049904526204',
            '36768208048819',

            # Maestro
            '5893433915020244',
            '6759761854174320',
            '6759998953884124',

            # Visa Electron
            '4026291468019846',
            '4844059039871494',
            '4913054050962393',

            # InstaPayment
            '6385037148943057',
            '6380659492219803',
            '6381454097795863',

            # Classic one
            '4111111111111111',
            '4242424242424242',
            '4444333322221111',
        )

    @classmethod
    def currency_provider(cls):
        return (
            'eur',
            'gbp',
            'usd',
        )

    @classmethod
    def http_code_provider(cls):
        return [
            (400, BadRequestError),
            (401, NotAuthorizedError),
            (402, PaymentRequiredError),
            (403, ForbiddenError),
            (404, NotFoundError),
            (405, MethodNotAllowedError),
            (406, NotAcceptableError),
            (407, ProxyAuthenticationRequiredError),
            (408, RequestTimeoutError),
            (409, ConflictError),
            (410, GoneError),
            (500, InternalServerError),
            (499, IliadHTTPClientError),
            (599, IliadHTTPServerError),
        ]

    @classmethod
    def iban_provider(cls):
        # Thanks Wikipedia
        return (
            'BE71 0961 2345 6769',
            'FR76 3000 6000 0112 3456 7890 189',
            'DE91 1000 0000 0123 4567 89',
            'GR9608100010000001234567890',
            'RO09 BCYP 0000 0012 3456 7890',
            'SA4420000001234567891234',
            'ES79 2100 0813 6101 2345 6789',
            'CH56 0483 5012 3456 7800 9 ',
            'GB98 MIDL 0700 9312 3456 78',
            'GB82WEST12345698765432',
        )
