# -*- coding: utf-8 -*-

from .base import BaseStatus


class RefundStatus(BaseStatus):
    """List of refund status."""

    NOT_HONORED = 'not_honored'
    PAYMENT_CANCELED = 'payment_canceled'
    REFUND_SENT = 'refund_sent'
    REFUNDED = 'refunded'
    TO_REFUND = 'to_refund'
