# -*- coding: utf-8 -*-

from stancer.status.base import BaseStatus


class MethodAllowed(BaseStatus):
    """List of methods allowed."""

    CARD = 'card'
    SEPA = 'sepa'
