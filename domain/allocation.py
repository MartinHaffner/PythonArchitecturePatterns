from .batch import Batch
from .order import OrderLine


class Allocation:
    @staticmethod
    def allocate_order_to_batch(batch: Batch, order_line: OrderLine) -> Batch:
        result = Batch(batch.reference, batch.sku, batch.number - order_line.number)
        return result
