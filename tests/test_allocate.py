from datetime import datetime, timedelta

import pytest
from domain.batch import Batch
from domain.order import OrderLine
from domain.service import OutOfStock, allocate


def test_allocate_one_batch():
    batch = Batch("r_123", "BLUE_LAMP", 20)
    order_line = OrderLine("o_123", "BLUE_LAMP", 2)
    result = allocate(order_line, [batch])
    assert result == batch.reference
    assert batch.remaining_size == 18


def test_allocate_multiple_one_in_store():
    batch_in_store = Batch("r_123", "BLUE_LAMP", 20)
    batch_due_tomorrow = Batch(
        "r_234", "BLUE_LAMP", 20, eta=datetime.today() + timedelta(days=1)
    )
    order_line = OrderLine("o_123", "BLUE_LAMP", 2)
    result = allocate(order_line, [batch_in_store, batch_due_tomorrow])
    assert result == batch_in_store.reference
    assert batch_in_store.remaining_size == 18
    assert batch_due_tomorrow.remaining_size == 20


def test_allocate_multiple_on_the_way():
    batch_due_today = Batch("r_234", "BLUE_LAMP", 20, eta=datetime.today())
    batch_due_tomorrow = Batch(
        "r_234", "BLUE_LAMP", 20, eta=datetime.today() + timedelta(days=1)
    )
    batch_due_later = Batch(
        "r_456", "BLUE_LAMP", 20, eta=datetime.today() + timedelta(days=7)
    )
    order_line = OrderLine("o_123", "BLUE_LAMP", 2)
    result = allocate(
        order_line, [batch_due_today, batch_due_tomorrow, batch_due_later]
    )
    assert result == batch_due_today.reference
    assert batch_due_today.remaining_size == 18
    assert batch_due_tomorrow.remaining_size == 20
    assert batch_due_later.remaining_size == 20


def test_allocate_multiple_different_on_the_way():
    batch_due_today = Batch("r_234", "RED_LAMP", 20, eta=datetime.today())
    batch_due_tomorrow = Batch(
        "r_234", "BLUE_LAMP", 20, eta=datetime.today() + timedelta(days=1)
    )
    batch_due_later = Batch(
        "r_456", "GREEN_LAMP", 20, eta=datetime.today() + timedelta(days=7)
    )
    order_line = OrderLine("o_123", "BLUE_LAMP", 2)
    result = allocate(
        order_line, [batch_due_today, batch_due_tomorrow, batch_due_later]
    )
    assert result == batch_due_tomorrow.reference
    assert batch_due_today.remaining_size == 20
    assert batch_due_tomorrow.remaining_size == 18
    assert batch_due_later.remaining_size == 20


def test_allocate_order_to_batch_mismatching_sku():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=2)
    batch = Batch(reference="b123", sku="BLUE-CHAIR", initial_size=20)
    with pytest.raises(OutOfStock):
        _ = allocate(order_line, [batch])


def test_allocate_order_to_batch_impossible():
    order_line = OrderLine(order_id="12345", sku="BLUE-CHAIR", number=20)
    batch = Batch(reference="b123", sku="BLUE-CHAIR", initial_size=20)
    result = allocate(order_line, [batch])
    assert result == batch.reference
    with pytest.raises(OutOfStock):
        _ = allocate(order_line, [batch])
