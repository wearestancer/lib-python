from stancer.core.decorators.populate_on_call import populate_on_call
from stancer.core.decorators.validate_type import validate_type
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

    def __init__(self) -> None:
        """Init internal data."""
        self._data: dict = {}
        self.method = None

    @property
    @populate_on_call
    def customer(self) -> Customer | None:
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
    def customer(self, value: Customer) -> None:
        self._data['customer'] = value
