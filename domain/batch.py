from dataclasses import dataclass


@dataclass(frozen=True)
class Batch:
    reference: str
    sku: str
    number: int
