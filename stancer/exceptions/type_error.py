# -*- coding: utf-8 -*-

from .base import StancerTypeError


class InvalidCardTokenizeError(StancerTypeError):
    """Raised when an invalid card tokenize status is used."""


class InvalidPaymentCaptureError(StancerTypeError):
    """Raised when an invalid capture is used."""
