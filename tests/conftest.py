import pytest
from repository.orm import mapper_registry, start_mappers
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
