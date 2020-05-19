# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from enum import Enum


class AuthStatus(Enum):
    """List of auth status"""

    ATTEMPTED = 'attempted'
    AVAILABLE = 'available'
    DECLINED = 'declined'
    EXPIRED = 'expired'
    FAILED = 'failed'
    REQUEST = 'request'
    REQUESTED = 'requested'
    SUCCESS = 'success'
    UNAVAILABLE = 'unavailable'
