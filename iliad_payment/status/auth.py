# -*- coding: utf-8 -*-

from .base import BaseStatus


class AuthStatus(BaseStatus):
    """List of auth status."""

    ATTEMPTED = 'attempted'
    AVAILABLE = 'available'
    DECLINED = 'declined'
    EXPIRED = 'expired'
    FAILED = 'failed'
    REQUEST = 'request'
    REQUESTED = 'requested'
    SUCCESS = 'success'
    UNAVAILABLE = 'unavailable'
