from typing import Dict

from .batch import Batch
from .order import OrderLine


class Allocation:
    allocated: Dict[str, str]

    def __init__(self) -> None:
        self.allocated = {}

    def allocate_order_to_batch(self, batch: Batch, order_line: OrderLine) -> Batch:
        if batch.sku != order_line.sku:
            raise ValueError("Batch SKU does not match OrderLine SKU!")
        if batch.number < order_line.number:
            raise ValueError("Batch number smaller than OrderLine number!")

        if order_line.order_id in self.allocated.keys():
            if self.allocated[order_line.order_id] == batch.reference:
                return batch  # already allocated to the same batch, ignore
            else:
                raise ValueError("Order already allocated to another batch")
        result = Batch(batch.reference, batch.sku, batch.number - order_line.number)
        self.allocated[order_line.order_id] = batch.reference
        return result
