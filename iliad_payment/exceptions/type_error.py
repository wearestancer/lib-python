# -*- coding: utf-8 -*-

from .base import IliadTypeError


class InvalidCardTokenizeError(IliadTypeError):
    """Raised when an invalid card tokenize status is used."""


class InvalidPaymentCaptureError(IliadTypeError):
    """Raised when an invalid capture is used."""
