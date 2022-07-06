"""Stub abstract object"""

from .stub_object import StubObject


class StubWithDefault(StubObject):
    _default_values = {
        'string1': 'Default value for string1',
    }
