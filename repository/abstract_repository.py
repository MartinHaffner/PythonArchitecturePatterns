import abc

from domain.batch import Batch


class AbstractRepository(abc.ABC):
    def add(self, batch: Batch):
        raise NotImplementedError

    def get(self, reference: str) -> Batch:
        raise NotImplementedError
