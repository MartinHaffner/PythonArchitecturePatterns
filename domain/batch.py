from datetime import datetime
from typing import Optional, Set

from .order import OrderLine


class Batch:
    reference: str
    sku: str
    initial_size: int
    remaining_size: int
    allocated: Set[OrderLine]
    eta: Optional[datetime]

    def __init__(
        self, reference: str, sku: str, initial_size: int, eta: datetime = None
    ):
        self.reference = reference
        self.sku = sku
        self.initial_size = initial_size
        self.remaining_size = initial_size
        self.allocated = set()
        self.eta = eta

    def __lt__(self, other: "Batch") -> bool:
        if self.eta is None:
            return True
        if other.eta is None:
            return False
        return self.eta < other.eta

    def __gt__(self, other: "Batch") -> bool:
        return not self.__lt__(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def can_allocate(self, order_line: OrderLine) -> bool:
        if self.sku != order_line.sku:
            return False
        if self.remaining_size < order_line.number:
            return False
        if order_line in self.allocated:
            return False
        return True

    def allocate_order_to_batch(self, order_line: OrderLine) -> None:
        if not self.can_allocate(order_line):
            return
        self.remaining_size -= order_line.number
        self.allocated.add(order_line)

    def can_dealllocate(self, order_line: OrderLine) -> bool:
        if order_line in self.allocated:
            return True
        return False

    def deallocate_order_from_batch(self, order_line: OrderLine) -> None:
        if not self.can_dealllocate(order_line):
            return
        self.remaining_size += order_line.number
        self.allocated.remove(order_line)
