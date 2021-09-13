def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (order_id, sku, number) "
        'VALUES ("o234", "BLUE-CHAIR", 20)'
    )
    [[order_line_id]] = session.execute(
        "SELECT id FROM order_lines WHERE order_id = :order_id AND sku = :sku",
        {"order_id": "o234", "sku": "BLUE-CHAIR"},
    )
    return order_line_id


def insert_batch(session):
    session.execute(
        "INSERT INTO batches (reference, sku, initial_size, remaining_size, eta) "
        'VALUES ("b234", "BLUE-CHAIR", 100, 100, NULL)'
    )
    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference = :reference_id AND sku = :sku",
        {"reference_id": "b234", "sku": "BLUE-CHAIR"},
    )
    return batch_id


def insert_allocation(session, order_line_id, batch_id):
    session.execute(
        "INSERT INTO allocations (order_line_id, batch_id) VALUES (:order_line_id, :batch_id)",
        {"order_line_id": order_line_id, "batch_id": batch_id},
    )
