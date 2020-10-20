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
    VersionNumber,
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
    def find_by_name(self, the_name):
        # type: (str) -> Optional[Project]
        raise NotImplementedError()


class AbstractProjectEntityRepository(AbstractRepository[T]):
    def find_by_project(self, project):
        # type: (KtrackId) -> List[T]
        raise NotImplementedError()

    def find_by_project_and_name(self, project, the_name):
        # type: (KtrackId, str) -> Optional[T]
        raise NotImplementedError()


class AssetRepository(AbstractProjectEntityRepository[Asset]):
    pass


class ShotRepository(AbstractProjectEntityRepository[Shot]):
    pass


class TaskRepository(AbstractProjectEntityRepository[Task]):
    pass


class WorkfileRepository(AbstractProjectEntityRepository[Workfile]):
    def find_by_task_and_version_number(self, task, version_number):
        # type: (KtrackId, VersionNumber) -> Optional[Workfile]
        raise NotImplementedError()

    def find_by_task_latest(self, task):
        # type: (KtrackId) -> Optional[Workfile]
        raise NotImplementedError()


class UserRepository(AbstractRepository[User]):
    pass


class PathEntryRepository(AbstractRepository[PathEntry]):
    def find_by_path(self, path):
        # type: (str) -> Optional[PathEntry]
        raise NotImplementedError()
