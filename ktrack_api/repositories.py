from typing import TypeVar, Generic, Iterable, Optional, List

from kttk.domain.entities import (
    Project,
    Asset,
    KtrackId,
    Shot,
    Task,
    Workfile,
    User,
    PathEntry,
)

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

    def delete(self, entity_id):
        # type: (KtrackId) -> None
        raise NotImplementedError()


class ProjectRepository(AbstractRepository[Project]):
    pass


class AbstractProjectEntityRepository(AbstractRepository[T]):
    def find_by_project(self, project):
        # type: (KtrackId) -> List[T]
        raise NotImplementedError()


class AssetRepository(AbstractProjectEntityRepository[Asset]):
    pass


class ShotRepository(AbstractProjectEntityRepository[Shot]):
    pass


class TaskRepository(AbstractProjectEntityRepository[Task]):
    pass


class WorkfileRepository(AbstractProjectEntityRepository[Workfile]):
    pass


class UserRepository(AbstractRepository[User]):
    pass


class PathEntryRepository(AbstractRepository[PathEntry]):

    def find_by_path(self, path):
        # type: (str) -> Optional[PathEntry]
        raise NotImplementedError()