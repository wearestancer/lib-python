# -*- coding: utf-8 -*-

from .core import AbstractAmount
from .core import AbstractObject


class Refund(AbstractObject, AbstractAmount):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'
