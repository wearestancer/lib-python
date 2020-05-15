# -*- coding: utf-8 -*-

from typing import Union
from urllib.parse import urlencode

from ..decorators import populate_on_call
from ..decorators import validate_type
from ...config import Config
from ...exceptions import InvalidUrlError
from ...exceptions import MissingApiKeyError
from ...exceptions import MissingPaymentIdError
from ...exceptions import MissingReturnUrlError


class PaymentPage(object):
    """Specific property and method for payment page."""

    _allowed_attributes = [
        'return_url',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}

    def payment_page_url(self, **kwargs) -> str:
        """
        External URL for Iliad payment page.

        You can pass parameters to the URL.

        For now we only handle `lang` and may be used to tell which language to use.
        If no language available matches the asked one, the page will be shown in english.

        Args:
            kwargs: Keyword argument use as URL parameters.

        Returns:
            Payment page URL for the current payment.

        Raises:
            MissingReturnUrlError: When you forgot to pass a return URL to receive the finalised payment.
            MissingPaymentIdError: When current payment has no ID, you may forgot to send it.
            MissingApiKeyError: When a public key was not found in your keychain.
        """

        if self.return_url is None:
            raise MissingReturnUrlError('You must provide a return URL before going to the payment page.')

        if self.id is None:
            message = (
                'A payment ID is mandatory to obtain a payment page URL.'
                ' '
                'Maybe you forgot to send the payment.'
            )

            raise MissingPaymentIdError(message)

        config = Config()

        if config.public_key is None:
            raise MissingApiKeyError('A public API key is needed to obtain a payment page URL.')

        if config.port is None:
            pattern = 'https://{host}/{key}/{id}'
        else:
            pattern = 'https://{host}:{port}/{key}/{id}'

        host = config.host.replace('api', 'payment')
        url = pattern.format(host=host, port=config.port, key=config.public_key, id=self.id)

        allowed = ('lang',)
        params = {x: kwargs[x] for x in kwargs if x in allowed}

        if params:
            return url + '?' + urlencode(params)

        return url

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
