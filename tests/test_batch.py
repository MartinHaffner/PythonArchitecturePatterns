from domain.batch import Batch


def test_create_batch():
    batch = Batch(reference="b123", sku="RED-CHAIR", number=20)
    assert batch.reference == "b123"
    assert batch.sku == "RED-CHAIR"
    assert batch.number == 20
