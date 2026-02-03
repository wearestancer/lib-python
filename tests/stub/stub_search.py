"""Stub abstract object with search"""

from stancer.core.abstract_object import AbstractObject
from stancer.core.abstract_search import AbstractSearch


class StubSearch(AbstractObject, AbstractSearch):
    _ENDPOINT = 'stub'

    @classmethod
    def filter_list_params(cls, **kwargs) -> dict:
        params = {}

        if 'foo' in kwargs:
            params['foo'] = kwargs.get('foo')

        return params
