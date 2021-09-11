from domain.batch import Batch
from domain.order import OrderLine


def test_create_batch():
    batch = Batch(reference="b123", sku="RED-CHAIR", initial_size=20)
    assert batch.reference == "b123"
    assert batch.sku == "RED-CHAIR"
    assert batch.initial_size == 20
    assert batch.remaining_size == 20


def _make_same_sku_items(sku, order_size, batch_size):
    order_line = OrderLine(order_id="o123", sku=sku, number=order_size)
    batch = Batch(reference="b123", sku=sku, initial_size=batch_size)
    return order_line, batch


def test_allocate_order_to_batch():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 2, 20)
    assert batch.can_allocate(order_line) is True
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.reference == batch.reference
    assert batch.sku == batch.sku
    assert batch.initial_size == 20
    assert batch.remaining_size == 18


def test_allocate_order_to_batch_equal_size():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 20, 20)
    assert batch.can_allocate(order_line) is True
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.reference == batch.reference
    assert batch.sku == batch.sku
    assert batch.initial_size == 20
    assert batch.remaining_size == 0


def test_allocate_order_to_batch_mismatching_sku():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="BLUE-CHAIR", initial_size=20)
    assert batch.can_allocate(order_line) is False
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.remaining_size == 20


def test_allocate_order_to_batch_insuffcient_number():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 25, 20)
    assert batch.can_allocate(order_line) is False
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.remaining_size == 20


def test_allocate_order_to_batch_twice():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 2, 20)
    assert batch.can_allocate(order_line) is True
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.reference == batch.reference
    assert batch.sku == batch.sku
    assert batch.remaining_size == 18
    assert batch.initial_size == 20
    assert batch.can_allocate(order_line) is False
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.remaining_size == 18


def test_deallocate_order_from_batch():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 2, 20)
    batch.allocate_order_to_batch(order_line=order_line)
    assert batch.can_dealllocate(order_line) is True
    batch.deallocate_order_from_batch(order_line=order_line)
    assert batch.reference == batch.reference
    assert batch.sku == batch.sku
    assert batch.initial_size == 20
    assert batch.remaining_size == 20
    assert batch.can_dealllocate(order_line) is False


def test_deallocate_order_never_allocated():
    order_line, batch = _make_same_sku_items("RED-CHAIR", 2, 20)
    assert batch.can_dealllocate(order_line) is False
    batch.deallocate_order_from_batch(order_line=order_line)
    assert batch.remaining_size == 20
