# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from enum import Enum


class PaymentStatus(Enum):
    """List of payment status"""

    AUTHORIZE = 'authorize'
    AUTHORIZED = 'authorized'
    CANCELED = 'canceled'
    CAPTURE = 'capture'
    CAPTURED = 'captured'
    DISPUTED = 'disputed'
    EXPIRED = 'expired'
    FAILED = 'failed'
    TO_CAPTURE = 'to_capture'
