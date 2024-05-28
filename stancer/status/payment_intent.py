# -*- coding: utf-8 -*-

from .base import BaseStatus


class PaymentIntentStatus(BaseStatus):
    """List of payment status."""

    REQUIRE_PAYMENT_METHOD = "require_payment_method"
    REQUIRE_AUTHENTICATION = "require_authentication"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    PROCESSING = "processing"
