import pytest
from domain.allocation import Allocation
from domain.batch import Batch
from domain.order import OrderLine


def test_allocate_order_to_batch():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="RED-CHAIR", number=20)
    result = Allocation().allocate_order_to_batch(batch=batch, order_line=order_line)
    assert result.reference == batch.reference
    assert result.sku == batch.sku
    assert result.number == 18


def test_allocate_order_to_batch_mismatching_sku():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="BLUE-CHAIR", number=20)
    with pytest.raises(ValueError):
        _ = Allocation().allocate_order_to_batch(batch=batch, order_line=order_line)


def test_allocate_order_to_batch_insuffcient_number():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=25)
    batch = Batch(reference="b123", sku="RED-CHAIR", number=20)
    with pytest.raises(ValueError):
        _ = Allocation().allocate_order_to_batch(batch=batch, order_line=order_line)


def test_allocate_order_to_batch_twice():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="RED-CHAIR", number=20)
    result = Allocation().allocate_order_to_batch(batch=batch, order_line=order_line)
    assert result.reference == batch.reference
    assert result.sku == batch.sku
    assert result.number == 18
    result = Allocation().allocate_order_to_batch(batch=batch, order_line=order_line)
    assert result.reference == batch.reference
    assert result.sku == batch.sku
    assert result.number == 18


def test_allocate_order_to_different_batches():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch_1 = Batch(reference="b123", sku="RED-CHAIR", number=20)
    batch_2 = Batch(reference="b234", sku="RED-CHAIR", number=20)
    alloc = Allocation()
    result = alloc.allocate_order_to_batch(batch=batch_1, order_line=order_line)
    assert result.reference == batch_1.reference
    assert result.sku == batch_1.sku
    assert result.number == 18
    with pytest.raises(ValueError):
        _ = alloc.allocate_order_to_batch(batch=batch_2, order_line=order_line)
