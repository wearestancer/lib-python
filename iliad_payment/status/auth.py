# -*- coding: utf-8 -*-

# pylint: disable=invalid-name


class AuthStatus(object):
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
