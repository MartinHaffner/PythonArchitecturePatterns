from domain.order import OrderLine


def test_init_orderline():
    order_line = OrderLine(order_id="12345", sku="RED-CHAIR", number=1)
    assert order_line.order_id == "12345"
    assert order_line.sku == "RED-CHAIR"
    assert order_line.number == 1
