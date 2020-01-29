# -*- coding: utf-8 -*-

from .core import AbstractObject


class Refund(AbstractObject):
    """Representation of a refund."""

    _ENDPOINT = 'refunds'
