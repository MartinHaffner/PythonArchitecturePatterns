from domain.batch import Batch
from domain.order import OrderLine
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255), nullable=False),
    Column("sku", String(255), nullable=False),
    Column("initial_size", Integer, nullable=False),
    Column("remaining_size", Integer, nullable=False),
    Column("eta", DateTime, nullable=True),
)

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255), nullable=False),
    Column("sku", String(255), nullable=False),
    Column("number", Integer, nullable=False),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    order_lines_mapper = mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            "allocated": relationship(
                order_lines_mapper, secondary=allocations, collection_class=set
            )
        },
    )
