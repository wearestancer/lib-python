# -*- coding: utf-8 -*-

from datetime import date
from typing import Any

from .core.abstract_country import AbstractCountry
from .core.abstract_deleted import AbstractDeleted
from .core.abstract_name import AbstractName
from .core.abstract_object import AbstractObject
from .core.decorators.populate_on_call import populate_on_call
from .core.decorators.validate_type import validate_type
from .core.helpers.coerce_uuid import coerce_uuid
from .exceptions import InvalidCustomerDateBirthError
from .exceptions import InvalidCustomerEmailError
from .exceptions import InvalidCustomerExternalIdError
from .exceptions import InvalidCustomerLegalIdError
from .exceptions import InvalidCustomerMobileError

try:
    from typing import override  # type: ignore
except ImportError:
    from typing_extensions import override


def validate_birth_date(value: str | date) -> date:
    """
    Transform the value in a valid date.

    Args:
        value: a date or a string that could be an invalid date.

    Return:
        A valid date object.

    Raises:
        InvalidCustomerDateBirthError: when the dateBirth is invalid.
    """
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InvalidCustomerDateBirthError from exc


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
    def date_birth(self) -> date | None:
        """
        Customer's birthdate.

        Args:
            value: Birthdate, must be a valid date.

        Return:
            The birthdate of the customer.

        Raises:
            InvalidCustomerDateBirthError: when the dateBirth is invalid.
        """
        return self._data.get('date_birth')

    @date_birth.setter
    @validate_type(
        date,
        throws=InvalidCustomerDateBirthError,
        coerce=validate_birth_date,
    )
    def date_birth(self, value: date) -> None:
        self._data['date_birth'] = value

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
            value (str): New ID, must be 36 characters max.

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

        Args:
            value: Customer's legal ID.

        Returns:
            The legal ID of the customer.

        Raises:
            InvalidCustomerLegalIdError: When legal ID is too long.
        """
        return self._data.get('legal_id')

    @legal_id.setter
    @validate_type(str, max=16, name='Legal ID', throws=InvalidCustomerLegalIdError)
    def legal_id(self, value: str) -> None:
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

    @override
    def to_json_repr(self) -> dict[str, Any] | str | bool:
        representation = super().to_json_repr()
        if (
            isinstance(representation, dict)
            and 'date_birth' in representation
            and isinstance(representation['date_birth'], date)
        ):
            representation['date_birth'] = representation['date_birth'].isoformat()
        return representation
