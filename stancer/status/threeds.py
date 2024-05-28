# -*- coding: utf-8 -*-

from .base import BaseStatus


class ThreedsStatus(BaseStatus):
    """List of payment status."""

    REQUIRED = 'required'
    NONE = 'none'
