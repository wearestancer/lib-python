# -*- coding: utf-8 -*-

from .base import BaseStatus


class MethodAllowed(BaseStatus):
    """List of methods allowed."""

    CARD = 'card'
    SEPA = 'sepa'
    APPLE_PAY = 'apple_pay'
