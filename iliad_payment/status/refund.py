# -*- coding: utf-8 -*-

from ..core.decorators import add_constant


@add_constant('not_honored', 'refund_sent', 'refunded', 'to_refund')
class _RefundStatus(object):
    """List of refund status"""

# pylint: disable=invalid-name
RefundStatus = _RefundStatus()
