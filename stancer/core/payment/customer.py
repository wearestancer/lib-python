from typing import Optional

from stancer.core.decorators import populate_on_call
from stancer.core.decorators import validate_type
from stancer.customer import Customer
from stancer.exceptions import InvalidCustomerError


class PaymentCustomer:
    """Specific customer property and method for all payments object"""

    _allowed_attributes = [
        'customer',
    ]
    _flat_attributes = [
        'customer',
    ]

    def __init__(self):
        """Init internal data."""
        self._data = {}
        self.id = None
        self.method = None

    @property
    @populate_on_call
    def customer(self) -> Optional[Customer]:
        """
        Customer handling the payment.

        Args:
            value (Customer): A valid `Customer` object.

        Returns:
            Customer: Customer handling the payment.

        Raises:
            InvalidCustomerError: When customer is invalid.
        """
        return self._data.get('customer')

    @customer.setter
    @validate_type(Customer, throws=InvalidCustomerError)
    def customer(self, value: Customer):
        self._data['customer'] = value
