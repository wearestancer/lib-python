"""Stub abstract object with search"""

from iliad_payment.core import AbstractObject
from iliad_payment.core import AbstractSearch


class StubSearch(AbstractObject, AbstractSearch):
    _ENDPOINT = 'stub'

    @classmethod
    def filter_list_params(cls, **kwargs) -> dict:
        params = {}

        if 'foo' in kwargs:
            params['foo'] = kwargs.get('foo')

        return params
