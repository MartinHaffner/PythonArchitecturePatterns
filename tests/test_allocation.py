from domain.allocation import Allocation
from domain.batch import Batch
from domain.order import OrderLine


def test_allocate_order_to_batch():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="RED-CHAIR", number=20)
    result = Allocation.allocate_order_to_batch(batch=batch, order_line=order_line)
    assert result.reference == batch.reference
    assert result.sku == batch.sku
    assert result.number == 18
