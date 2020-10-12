# -*- coding: utf-8 -*-

from .core import AbstractObject
from .core.decorators import populate_on_call


class Dispute(AbstractObject):
    """Representation of a dispute."""
