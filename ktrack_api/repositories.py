from typing import TypeVar, Generic, Iterable, Optional

from kttk.domain.entities import Project

T = TypeVar('T')
ID = TypeVar('ID')


class AbstractRepository(Generic[T, ID]):

    def find_one(self, the_id):
        # type: (ID) -> Optional[T]
        raise NotImplementedError()

    def find_all(self):
        # type: () -> Iterable[T]
        raise NotImplementedError()

    def save(self, entity):
        # type: (T) -> T
        raise NotImplementedError()

    def save_all(self, entities):
        # type: (Iterable[T]) -> Iterable[T]
        raise NotImplementedError()


class ProjectRepository(AbstractRepository[Project, ID]):
    pass
