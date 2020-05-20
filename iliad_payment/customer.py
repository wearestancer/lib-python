# -*- coding: utf-8 -*-

from .core import AbstractCountry
from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .core.helpers import coerce_uuid
from .exceptions import InvalidCustomerEmailError
from .exceptions import InvalidCustomerExternalIdError
from .exceptions import InvalidCustomerMobileError


class Customer(AbstractObject, AbstractName, AbstractCountry):
    """Representation of a customer."""

    _ENDPOINT = 'customers'

    _allowed_attributes = [
        'email',
        'external_id',
        'mobile',
    ]

    @property
    @populate_on_call
    def email(self) -> str:
        """
        Customer's email.

        Args:
            value (str): New email, must be between 5 and 64 characters.

        Returns:
            str: Customer's email.

        Raises:
            InvalidCustomerEmailError: When email is invalid.
        """
        return self._data.get('email')

    @email.setter
    @validate_type(str, min=5, max=64, throws=InvalidCustomerEmailError)
    def email(self, value: str):
        self._data['email'] = value

    @property
    @populate_on_call
    def external_id(self) -> str:
        """
        Customer's external ID.

        External for the API, you can store your customer's identifier here.

        Args:
            value (str): New ID, must be between 36 characters max.

        Returns:
            str: Customer's external ID.

        Raises:
            InvalidCustomerExternalIdError: When external ID is invalid.
        """
        return self._data.get('external_id')

    @external_id.setter
    @validate_type(
        str,
        coerce=coerce_uuid,
        max=36,
        name='External ID',
        throws=InvalidCustomerExternalIdError,
    )
    def external_id(self, value: str):
        self._data['external_id'] = value

    @property
    def is_complete(self) -> bool:
        """
        Indicate if all mandatory customer data are provided.

        Returns:
            Is the customer complete ?
        """
        if self.email is None and self.mobile is None:
            return False

        return True

    @property
    @populate_on_call
    def mobile(self) -> str:
        """
        Customer's mobile phone number.

        Args:
            value (str): New mobile, must be between 8 and 16 characters.

        Returns:
            str: Customer's mobile phone number.

        Raises:
            InvalidCustomerMobileError: When mobile phone number is invalid.
        """
        return self._data.get('mobile')

    @mobile.setter
    @validate_type(
        str,
        min=8,
        max=16,
        name='Mobile phone',
        throws=InvalidCustomerMobileError,
    )
    def mobile(self, value: str):
        self._data['mobile'] = value
