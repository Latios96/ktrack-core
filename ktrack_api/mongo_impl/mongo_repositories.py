from collections import Iterable

from typing import Optional, List, TypeVar, Generic, Type

from ktrack_api.exceptions import EntityNotFoundException
from ktrack_api.mongo_impl.entities import (
    Project as MongoProject,
    Asset as MongoAsset,
    PathEntry as MongoPathEntry,
    Task as MongoTask,
    Shot as MongoShot,
    WorkFile as MongoWorkfile,
)
from ktrack_api.repositories import (
    ProjectRepository,
    AssetRepository,
    PathEntryRepository,
    TaskRepository,
    ShotRepository,
    WorkfileRepository,
)
from kttk.context import Context
from kttk.domain.entities import (
    Project,
    Thumbnail,
    Asset,
    KtrackId,
    PathEntry,
    Task,
    EntityLink,
    Shot,
    CutInformation,
    Workfile,
    VersionNumber,
)

T = TypeVar("T")
MONGO_T = TypeVar("MONGO_T")


class AbstractMongoRepository(Generic[T, MONGO_T]):
    def mongo_entity(self):
        # type: () -> Type[MONGO_T]
        raise NotImplementedError()

    def to_mongo_entity(self, domain_entity):
        # type: (T) -> MONGO_T
        raise NotImplementedError()

    def to_domain_entity(self, mongo_entity):
        # type: (MONGO_T) -> T
        raise NotImplementedError()

    def find_one(self, the_id):
        # type: (KtrackId) -> Optional[T]
        mongo_entity = self.mongo_entity().objects(id=the_id).first()
        return self.to_domain_entity(mongo_entity)

    def find_all(self):
        # type: () -> Iterable[T]
        return list(map(self.to_domain_entity, self.mongo_entity().objects.all()))

    def save(self, entity):
        # type: (T) -> T
        mongo_entity = self.to_mongo_entity(entity)
        mongo_entity.save()
        return self.to_domain_entity(mongo_entity)

    def save_all(self, entities):
        # type: (Iterable[T]) -> Iterable[T]
        return list(map(self.save, entities))

    def delete(self, entity_id):
        # type: (KtrackId) -> None
        entity_candidates = self.mongo_entity().objects(id=entity_id).all()
        entity_candidates.delete()


class AbstractMongoProjectEntityRepository(AbstractMongoRepository[T, MONGO_T]):
    def find_by_project(self, domain_entity):
        # type: (KtrackId) -> List[T]
        mongo_entity = self.mongo_entity().objects(project__id=domain_entity).all()
        return list(map(self.to_domain_entity, mongo_entity))

    def find_by_project_and_name(self, project, name):
        # type: (KtrackId,str) -> Optional[T]
        mongo_entity = self.mongo_entity().objects(project=project, name=name).first()
        return self.to_domain_entity(mongo_entity)


class MongoProjectRepository(
    AbstractMongoRepository[Project, MongoProject], ProjectRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoProject]
        return MongoProject

    def find_by_name(self, the_name):
        # type: (str) -> Optional[T]
        mongo_entity = self.mongo_entity().objects(name=the_name).first()
        return self.to_domain_entity(mongo_entity)

    def to_mongo_entity(self, domain_entity):
        # type: (Project) -> MongoProject
        if domain_entity:
            return MongoProject(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                thumbnail={"path": domain_entity.thumbnail.path}
                if domain_entity.thumbnail
                else {},
                name=domain_entity.name,
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoProject) -> Project
        if mongo_entity:
            return Project(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                thumbnail=Thumbnail(path=mongo_entity.thumbnail.get("path")),
                name=mongo_entity.name,
            )


class MongoAssetRepository(
    AbstractMongoProjectEntityRepository[Asset, MongoAsset], AssetRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoAsset]
        return MongoAsset

    def find_by_name(self, the_name):
        # type: (str) -> Optional[T]
        mongo_entity = self.mongo_entity().objects(code=the_name).first()
        return self.to_domain_entity(mongo_entity)

    def find_by_project_and_name(self, project, name):
        # type: (KtrackId,str) -> Optional[T]
        mongo_entity = (
            self.mongo_entity().objects(project__id=project, code=name).first()
        )
        return self.to_domain_entity(mongo_entity)

    def to_mongo_entity(self, domain_entity):
        # type: (Asset) -> MongoAsset
        if domain_entity:
            return MongoAsset(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                thumbnail={"path": domain_entity.thumbnail.path}
                if domain_entity.thumbnail
                else {},
                code=domain_entity.name,
                asset_type=domain_entity.asset_type,
                project={"type": "project", "id": domain_entity.project}
                if domain_entity.project
                else None,
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoAsset) -> Asset
        if mongo_entity:
            return Asset(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                thumbnail=Thumbnail(path=mongo_entity.thumbnail.get("path")),
                name=mongo_entity.code,
                asset_type=mongo_entity.asset_type,
                project=mongo_entity.project["id"],
            )


class MongoShotRepository(
    AbstractMongoProjectEntityRepository[Shot, MongoShot], ShotRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoShot]
        return MongoShot

    def find_by_name(self, the_name):
        # type: (str) -> Optional[T]
        mongo_entity = self.mongo_entity().objects(code=the_name).first()
        return self.to_domain_entity(mongo_entity)

    def find_by_project_and_name(self, project, name):
        # type: (KtrackId,str) -> Optional[T]
        mongo_entity = (
            self.mongo_entity().objects(project__id=project, code=name).first()
        )
        return self.to_domain_entity(mongo_entity)

    def to_mongo_entity(self, domain_entity):
        # type: (Shot) -> MongoShot
        if domain_entity:
            return MongoShot(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                thumbnail={"path": domain_entity.thumbnail.path}
                if domain_entity.thumbnail
                else {},
                code=domain_entity.code,
                project={"type": "project", "id": domain_entity.project}
                if domain_entity.project
                else None,
                cut_in=domain_entity.cut_information.cut_in,
                cut_out=domain_entity.cut_information.cut_out,
                cut_duration=domain_entity.cut_information.cut_duration,
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoShot) -> Shot
        if mongo_entity:
            return Shot(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                thumbnail=Thumbnail(path=mongo_entity.thumbnail.get("path")),
                code=mongo_entity.code,
                project=mongo_entity.project["id"],
                cut_information=CutInformation(
                    cut_in=mongo_entity.cut_in, cut_out=mongo_entity.cut_out
                ),
            )


class MongoPathEntryRepository(
    AbstractMongoRepository[PathEntry, MongoPathEntry], PathEntryRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoPathEntry]
        return MongoPathEntry

    def to_mongo_entity(self, domain_entity):
        # type: (PathEntry) -> MongoPathEntry
        if domain_entity:
            return MongoPathEntry(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                path=domain_entity.path,
                context=domain_entity.context.as_dict(),
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoPathEntry) -> PathEntry
        if mongo_entity:
            return PathEntry(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                path=mongo_entity.path,
                context=Context.from_dict(mongo_entity.context),
            )

    def find_by_path(self, path):
        # type: (str) -> Optional[PathEntry]
        mongo_entity = self.mongo_entity().objects(path=path).first()
        return self.to_domain_entity(mongo_entity)


class MongoTaskRepository(
    AbstractMongoProjectEntityRepository[Task, MongoTask], TaskRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoTask]
        return MongoTask

    def find_by_project_and_entity_name(self, project, entity_type, entity_name):
        print(project, entity_type, entity_name)
        if entity_type == "asset":
            entity = MongoAsset.objects(project__id=project, code=entity_name).first()
            if not entity:
                return None
            task = self.mongo_entity().objects(entity__id=str(entity.id)).first()
        else:
            entity = MongoShot.objects(project__id=project, code=entity_name).first()
            if not entity:
                return None
            task = self.mongo_entity().objects(entity__id=str(entity.id)).first()

        entity = self.to_domain_entity(task)
        return entity

    def to_mongo_entity(self, domain_entity):
        # type: (Task) -> MongoTask
        if domain_entity:
            return MongoTask(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                project={"type": "project", "id": domain_entity.project}
                if domain_entity.project
                else None,
                name=domain_entity.name,
                step=domain_entity.step,
                entity={
                    "type": domain_entity.entity.type,
                    "id": domain_entity.entity.id,
                },
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoTask) -> Task
        if mongo_entity:
            return Task(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                project=mongo_entity.project["id"],
                name=mongo_entity.name,
                step=mongo_entity.step,
                entity=EntityLink(
                    id=mongo_entity.entity["id"], type=mongo_entity.entity["type"]
                ),
            )


class MongoWorkfileRepository(
    AbstractMongoProjectEntityRepository[Workfile, MongoWorkfile], WorkfileRepository
):
    def find_by_task_and_version_number(self, task, version_number):
        # type: (KtrackId, VersionNumber) -> Optional[Workfile]
        mongo_entity = (
            self.mongo_entity()
            .objects(
                entity={"type": "task", "id": task},
                version_number=version_number.number,
            )
            .all()
        )
        return list(map(self.to_domain_entity, mongo_entity))

    def find_by_task_latest(self, task):
        # type: (KtrackId) -> Optional[Workfile]
        entities = (
            self.mongo_entity().objects(entity={"type": "task", "id": task}).all()
        )
        if not entities:
            return None
        latest = max(entities, key=lambda x: x.version_number)
        return self.to_domain_entity(latest)

    def mongo_entity(self):
        # type: () -> Type[MongoWorkfile]
        return MongoWorkfile

    def to_mongo_entity(self, domain_entity):
        # type: (Workfile) -> MongoWorkfile
        if domain_entity:
            return MongoWorkfile(
                id=domain_entity.id,
                created_at=domain_entity.created_at,
                updated_at=domain_entity.updated_at,
                project={"type": "project", "id": domain_entity.project}
                if domain_entity.project
                else None,
                name=domain_entity.name,
                entity={
                    "type": domain_entity.entity.type,
                    "id": domain_entity.entity.id,
                },
                path=domain_entity.path,
                comment=domain_entity.comment,
                version_number=domain_entity.version_number.number,
                created_from=domain_entity.created_from,
            )

    def to_domain_entity(self, mongo_entity):
        # type: (MongoWorkfile) -> Workfile
        if mongo_entity:
            return Workfile(
                id=KtrackId(mongo_entity.id),
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                project=mongo_entity.project["id"],
                name=mongo_entity.name,
                entity=EntityLink(
                    id=mongo_entity.entity["id"], type=mongo_entity.entity["type"]
                ),
                path=mongo_entity.path,
                comment=mongo_entity.comment,
                version_number=VersionNumber(mongo_entity.version_number),
                created_from=KtrackId(mongo_entity.created_from)
                if mongo_entity.created_from
                else None,
            )
