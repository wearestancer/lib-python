# -*- coding: utf-8 -*-

from ..core.decorators import add_constant


@add_constant(
    'authorize',
    'authorized',
    'canceled',
    'capture',
    'captured',
    'disputed',
    'expired',
    'failed',
    'to_capture',
)
class _PaymentStatus(object):
    """List of payment status"""

# pylint: disable=invalid-name
PaymentStatus = _PaymentStatus()
