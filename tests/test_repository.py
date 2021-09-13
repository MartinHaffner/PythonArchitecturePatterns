from domain.batch import Batch
from repository.sqlalchemy_repository import SQLAlchemyRepository
from testutils import insert_allocation, insert_batch, insert_order_line


def test_repository_save_batch(session):
    batch = Batch(reference="ref123", sku="RED-CHAIR", initial_size=100)
    repo = SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()
    result = session.execute(
        "SELECT reference, sku, initial_size, remaining_size, eta FROM batches"
    )
    assert list(result) == [("ref123", "RED-CHAIR", 100, 100, None)]


def test_repository_load_batch(session):
    order_line_id = insert_order_line(session)
    batch_id = insert_batch(session)
    insert_allocation(session, order_line_id, batch_id)

    repo = SQLAlchemyRepository(session)
    result = repo.get("b234")
    assert result.reference == "b234"
    assert result.sku == "BLUE-CHAIR"
    assert len(result.allocated) == 1
    assert next(iter(result.allocated)).order_id == "o234"
