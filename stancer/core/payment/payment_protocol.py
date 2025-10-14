from typing import Any
from typing import Protocol


class PaymentProtocol(Protocol):
    """Protocol that define which attribute has to be implemented for Payment Objects"""

    _allowed_attributes: list[str]
    _data: dict[str, Any]
    amount: int | None
    currency: str | None
    _populated: bool
    id: str | None
    method: str | None

    def populate(self: Any) -> Any: ...
