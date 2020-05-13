# -*- coding: utf-8 -*-

from typing import Union

from ..decorators import populate_on_call
from ..decorators import validate_type
from ...exceptions import InvalidUrlError


class PaymentPage(object):
    """Specific property and method for payment page."""

    _allowed_attributes = [
        'return_url',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}

    @property
    @populate_on_call
    def return_url(self) -> str:
        """
        URL used to return to your store when using the payment page.

        Args:
            value: A valid HTTPS URL.

        Returns:
            URL used on payment return.

        Raises:
            InvalidUrlError: When URL is invalid.
        """
        return self._data.get('return_url')

    @return_url.setter
    @validate_type(
        str,
        name='Return URL',
        validation=lambda v: None if v.startswith('https://') else 'Return URL must use HTTPS protocol.',
        throws=InvalidUrlError,
    )
    def return_url(self, value: str):
        self._data['return_url'] = value
