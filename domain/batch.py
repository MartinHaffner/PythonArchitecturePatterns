from typing import Dict

from .order import OrderLine


class Batch:
    reference: str
    sku: str
    initial_size: int
    remaining_size: int
    allocated: Dict[str, str]

    def __init__(self, reference: str, sku: str, initial_size: int):
        self.reference = reference
        self.sku = sku
        self.initial_size = initial_size
        self.remaining_size = initial_size
        self.allocated = {}

    def can_allocate(self, order_line: OrderLine) -> bool:
        if self.sku != order_line.sku:
            return False
        if self.remaining_size < order_line.number:
            return False
        if order_line.order_id in self.allocated.keys():
            return False
        return True

    def allocate_order_to_batch(self, order_line: OrderLine) -> None:
        if not self.can_allocate(order_line):
            raise ValueError("Cannot allocate this order_line to this batch")
        self.remaining_size -= order_line.number
        self.allocated[order_line.order_id] = self.reference
