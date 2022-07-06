# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

# pylint: enable=missing-docstring
from datetime import date
import pytest
from random import choice, randint
import string

from stancer import Config
from stancer.exceptions import *  # pylint: disable=wildcard-import


class TestHelper(object):
    """Add some helper for tests."""

    def setup_method(self, method):
        conf = Config()

        conf.keys = 'stest_' + self.random_string(24)

        del conf.default_timezone

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

    def random_timezone(self):
        zones = [
            'UTC',
            'America/Phoenix',
            'Atlantic/Bermuda',
            'Australia/Melbourne',
            'Europe/Paris',
        ]

        return choice(zones)

    def random_year(self):
        return self.random_integer(1, 20) + self.current_year

    @property
    def current_year(self):
        return date.today().year

    @classmethod
    def api_key_provider(cls):
        obj = TestHelper()

        return obj.public_api_key_provider() + obj.secret_api_key_provider()

    @classmethod
    def public_api_key_provider(cls):
        obj = TestHelper()

        return [
            ('pprod_' + obj.random_string(24), Config.LIVE_MODE, 'pprod'),
            ('ptest_' + obj.random_string(24), Config.TEST_MODE, 'ptest'),
        ]

    @classmethod
    def secret_api_key_provider(cls):
        obj = TestHelper()

        return [
            ('sprod_' + obj.random_string(24), Config.LIVE_MODE, 'sprod'),
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
    def currency_provider(cls, one=False):
        currencies = (
            'eur',
            'gbp',
            'usd',
        )

        if one:
            return choice(currencies)

        return currencies

    @classmethod
    def http_code_provider(cls):
        return [
            (400, BadRequestError),
            (401, UnauthorizedError),
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
            (499, StancerHTTPClientError),
            (599, StancerHTTPServerError),
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

    @classmethod
    def ip_provider(cls, one=False):
        ips = cls.ipv4_provider() + cls.ipv6_provider()

        if one:
            return choice(ips)

        return ips

    @classmethod
    def ipv4_provider(cls):  # 7 addresses
        return [
            '212.27.48.10',  # www.free.fr
            '216.58.206.238',  # www.google.com
            '17.178.96.59',  # www.apple.com
            '17.142.160.59',  # www.apple.com
            '17.172.224.47',  # www.apple.com
            '179.60.192.36',  # www.facebook.com
            '198.41.0.4',  # a.root-servers.org
        ]

    @classmethod
    def ipv6_provider(cls):  # 9 addresses
        return [
            '2a01:0e0c:0001:0000:0000:0000:0000:0001',  # www.free.fr
            '2a01:e0c:1:0:0:0:0:1',  # www.free.fr
            '2a01:e0c:1::1',  # www.free.fr
            '2a00:1450:4007:080f:0000:0000:0000:200e',  # www.google.com
            '2a00:1450:4007:80f::200e',  # www.google.com
            '2a03:2880:f11f:0083:face:b00c:0000:25de',  # www.facebook.com
            '2a03:2880:f11f:83:face:b00c:0:25de',  # www.facebook.com
            '2001:0503:ba3e:0000:0000:0000:0002:0030',  # a.root-servers.org
            '2001:503:ba3e::2:30',  # a.root-servers.org
        ]
