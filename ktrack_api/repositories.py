from typing import TypeVar, Generic, Iterable, Optional, List

from kttk.domain.entities import Project, Asset, KtrackId

T = TypeVar("T")


class AbstractRepository(Generic[T]):
    def find_one(self, the_id):
        # type: (KtrackId) -> Optional[T]
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


class ProjectRepository(AbstractRepository[Project]):
    pass


class AssetRepository(AbstractRepository[Asset]):
    def find_by_project(self, project):
        # type: (KtrackId) -> List[Asset]
        raise NotImplementedError()
