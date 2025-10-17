from typing import Any
from typing import Protocol

try:
    # Self is available in Python 3.11
    from typing import Self  # type: ignore
except ImportError:
    from typing import TypeVar

    Self = TypeVar('Self', bound='PaymentProtocol')  # type: ignore


class PaymentProtocol(Protocol):
    """Protocol that define which attribute has to be implemented for Payment Objects"""

    _allowed_attributes: list[str]
    _data: dict[str, Any]
    _populated: bool
    amount: int | None
    currency: str | None
    id: str | None
    method: str | None

    def populate(self: Self) -> Self: ...
