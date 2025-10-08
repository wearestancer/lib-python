from abc import ABC

from stancer.core.decorators.populate_on_call import populate_on_call
from stancer.core.decorators.validate_type import validate_type
from stancer.core.payment.payment_protocol import PaymentProtocol
from stancer.exceptions import InvalidSepaError
from stancer.sepa import Sepa


class PaymentSepa(ABC, PaymentProtocol):
    _allowed_attributes = [
        'sepa',
    ]
    _flat_attributes = [
        'sepa',
    ]

    def __init__(self) -> None:
        """Init internal data."""
        self._data = {}
        self.method = None

    @property
    @populate_on_call
    def sepa(self) -> Sepa | None:
        """
        Source SEPA account for the payment.

        Args:
            value (Sepa): A valid `Sepa` object.

        Returns:
            Sepa: SEPA used for the payment.

        Raises:
            InvalidSepaError: When sepa is invalid.
        """
        return self._data.get('sepa')

    @sepa.setter
    @validate_type(Sepa, throws=InvalidSepaError)
    def sepa(self, value: Sepa) -> None:
        self._data['sepa'] = value
        self._data['method'] = 'sepa'
