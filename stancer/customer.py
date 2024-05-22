# -*- coding: utf-8 -*-

import datetime

from .core import AbstractCountry
from .core import AbstractDeleted
from .core import AbstractName
from .core import AbstractObject
from .core.decorators import populate_on_call
from .core.decorators import validate_type
from .core.helpers import coerce_uuid
from .exceptions import InvalidCustomerEmailError
from .exceptions import InvalidCustomerExternalIdError
from .exceptions import InvalidCustomerMobileError
from .exceptions import InvalidCustomerDateBirthError
from .exceptions import InvalidCustomerLegalIdError


class Customer(AbstractObject, AbstractName, AbstractCountry, AbstractDeleted):
    """Representation of a customer."""

    _ENDPOINT = 'customers'

    _allowed_attributes = [
        'date_birth',
        'email',
        'external_id',
        'legal_id',
        'mobile',
    ]

    @property
    @populate_on_call
    def date_birth(self) -> str | None:
        """
        Customer's birthdate.

        Return the birthdate of the customer
        """
        return self._data.get('date_birth')

    @date_birth.setter
    @validate_type(str, min=10, max=10, throws=InvalidCustomerDateBirthError)
    def date_birth(self, value: str):
        self._data['date_birth'] = str(datetime.date.fromisoformat(value))

    @property
    @populate_on_call
    def email(self) -> str | None:
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
    def email(self, value: str) -> None:
        self._data['email'] = value

    @property
    @populate_on_call
    def external_id(self) -> str | None:
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
    def external_id(self, value: str) -> None:
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
    def legal_id(self) -> str | None:
        """
        Customer's legal identification ( SIREN, CBE, KVK, ...).

        Returns:
            The legal Id of the customer
        """
        return self._data.get('legal_id')

    @legal_id.setter
    @validate_type(str, max=16, name='Legal ID', throws=InvalidCustomerLegalIdError)
    def legal_id(self, value: str):
        self._data['legal_id'] = value

    @property
    @populate_on_call
    def mobile(self) -> str | None:
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
    def mobile(self, value: str) -> None:
        self._data['mobile'] = value
