"""Stub abstract object with search"""

from iliad_payment.core import AbstractObject
from iliad_payment.core import AbstractSearch


class StubSearch(AbstractObject, AbstractSearch):
    _ENDPOINT = 'stub'
