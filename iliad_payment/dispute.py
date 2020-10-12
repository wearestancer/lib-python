# -*- coding: utf-8 -*-

from .core import AbstractAmount
from .core import AbstractObject
from .core.decorators import populate_on_call


class Dispute(AbstractObject, AbstractAmount):
    """Representation of a dispute."""
