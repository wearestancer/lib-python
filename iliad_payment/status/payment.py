# -*- coding: utf-8 -*-

from .base import BaseStatus


class PaymentStatus(BaseStatus):
    """List of payment status."""

    AUTHORIZE = 'authorize'
    AUTHORIZED = 'authorized'
    CANCELED = 'canceled'
    CAPTURE = 'capture'
    CAPTURED = 'captured'
    DISPUTED = 'disputed'
    EXPIRED = 'expired'
    FAILED = 'failed'
    TO_CAPTURE = 'to_capture'
