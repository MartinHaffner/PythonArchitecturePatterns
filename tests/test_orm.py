import datetime

from domain.batch import Batch
from domain.order import OrderLine
from testutils import insert_allocation, insert_batch, insert_order_line


def test_save_batches(session):
    batch = Batch(
        reference="b123",
        sku="RED-CHAIR",
        initial_size=100,
        eta=datetime.datetime(year=2021, month=9, day=13, hour=12, minute=0, second=0),
    )
    session.add(batch)
    session.commit()
    rows = session.execute(
        'SELECT reference, sku, initial_size, remaining_size, eta FROM "batches"'
    )
    assert list(rows) == [("b123", "RED-CHAIR", 100, 100, "2021-09-13 12:00:00.000000")]


def test_retrieve_batches(session):
    session.execute(
        "INSERT INTO batches (reference, sku, initial_size, remaining_size, eta) "
        'VALUES ("b234", "RED-CHAIR", 100, 80, NULL)'
    )
    [result] = session.query(Batch).all()
    assert result.reference == "b234"
    assert result.sku == "RED-CHAIR"
    assert result.eta is None
    assert result.initial_size == 100
    assert result.remaining_size == 80


def test_save_order_lines(session):
    order_line = OrderLine(order_id="o123", sku="RED-CHAIR", number=20)
    session.add(order_line)
    session.commit()
    rows = session.execute('SELECT order_id, sku, number FROM "order_lines"')
    assert list(rows) == [("o123", "RED-CHAIR", 20)]


def test_retrieve_order_lines(session):
    session.execute(
        "INSERT INTO order_lines (order_id, sku, number) "
        'VALUES ("o234", "RED-CHAIR", 20)'
    )
    expected = [
        OrderLine(order_id="o234", sku="RED-CHAIR", number=20),
    ]
    result = session.query(OrderLine).all()
    assert result == expected
    assert result[0].sku == expected[0].sku
    assert result[0].number == expected[0].number


def test_save_allocations(session):
    batch = Batch(
        reference="b123",
        sku="RED-CHAIR",
        initial_size=100,
        eta=datetime.datetime(year=2021, month=9, day=13, hour=12, minute=0, second=0),
    )
    order_line = OrderLine(order_id="o123", sku="RED-CHAIR", number=20)
    batch.allocate_order_to_batch(order_line=order_line)
    session.add(batch)
    session.commit()
    rows = session.execute('SELECT order_line_id, batch_id FROM "allocations"')
    assert list(rows) == [(order_line.id, batch.id)]


def test_retrieve_allocations(session):
    order_line_id = insert_order_line(session)
    batch_id = insert_batch(session)
    insert_allocation(session, order_line_id, batch_id)

    batch = session.query(Batch).one()
    assert batch.reference == "b234"
    assert batch.sku == "BLUE-CHAIR"
    assert len(batch.allocated) == 1
    assert next(iter(batch.allocated)).order_id == "o234"
