# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from enum import Enum


class RefundStatus(Enum):
    """List of refund status"""

    NOT_HONORED = 'not_honored'
    PAYMENT_CANCELED = 'payment_canceled'
    REFUND_SENT = 'refund_sent'
    REFUNDED = 'refunded'
    TO_REFUND = 'to_refund'
