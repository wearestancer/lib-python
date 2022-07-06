# -*- coding: utf-8 -*-

from typing import Optional
from urllib.parse import urlencode

from ..decorators import populate_on_call
from ..decorators import validate_type
from ...config import Config
from ...exceptions import InvalidUrlError
from ...exceptions import MissingApiKeyError
from ...exceptions import MissingPaymentIdError
from ...exceptions import MissingReturnUrlError


def _valid_retur_url(value) -> Optional[str]:
    if value.startswith('https://'):
        return None

    return 'Return URL must use HTTPS protocol.'


class PaymentPage(object):
    """Specific property and method for payment page."""

    _allowed_attributes = [
        'return_url',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}
        self.id = None  # pylint: disable=invalid-name

    def payment_page_url(self, **kwargs) -> str:
        """
        External URL for Stancer payment page.

        You can pass parameters to the URL.

        For now we only handle `lang` and may be used to tell which
        language to use.
        If no language available matches the asked one,
        the page will be shown in english.

        Args:
            kwargs: Keyword argument use as URL parameters.

        Returns:
            Payment page URL for the current payment.

        Raises:
            MissingReturnUrlError: When you forgot to pass a return URL
                to receive the finalised payment.
            MissingPaymentIdError: When current payment has no ID,
                you may forgot to send it.
            MissingApiKeyError: When a public key was not found in
                your keychain.
        """

        if self.return_url is None:
            message = (
                'You must provide a return URL'
                ' '
                'before going to the payment page.'
            )

            raise MissingReturnUrlError(message)

        if self.id is None:
            message = (
                'A payment ID is mandatory to obtain a payment page URL.'
                ' '
                'Maybe you forgot to send the payment.'
            )

            raise MissingPaymentIdError(message)

        config = Config()

        if config.public_key is None:
            message = (
                'A public API key is needed to obtain a payment page URL.'
            )

            raise MissingApiKeyError(message)

        if config.port is None:
            pattern = 'https://{host}/{key}/{id}'
        else:
            pattern = 'https://{host}:{port}/{key}/{id}'

        tmp = {
            'host': config.host.replace('api', 'payment'),
            'id': self.id,
            'key': config.public_key,
            'port': config.port,
        }
        url = pattern.format(**tmp)

        allowed = ('lang',)
        params = { k: v for k, v in kwargs.items() if k in allowed }

        if params:
            return url + '?' + urlencode(params)

        return url

    @property
    @populate_on_call
    def return_url(self) -> Optional[str]:
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
        validation=_valid_retur_url,
        throws=InvalidUrlError,
    )
    def return_url(self, value: str):
        self._data['return_url'] = value
