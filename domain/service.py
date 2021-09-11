from typing import List

from .batch import Batch
from .order import OrderLine


class OutOfStock(Exception):
    pass


def allocate(order_line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(order_line)
        )
        batch.allocate_order_to_batch(order_line)
        return batch.reference
    except StopIteration:
        raise OutOfStock
