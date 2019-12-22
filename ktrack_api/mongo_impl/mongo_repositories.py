from collections import Iterable

from typing import Optional, List, TypeVar, Generic, Type

from ktrack_api.mongo_impl.entities import Project as MongoProject, Asset as MongoAsset
from ktrack_api.repositories import ProjectRepository, AssetRepository
from kttk.domain.entities import Project, Thumbnail, Asset, KtrackId

T = TypeVar("T")
MONGO_T = TypeVar("MONGO_T")


class AbstractMongoNonProjectEntityRepository(Generic[T, MONGO_T]):
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
        mongo_project = self.to_mongo_entity(entity)
        mongo_project.save()
        return self.to_domain_entity(mongo_project)

    def save_all(self, entities):
        # type: (Iterable[T]) -> Iterable[T]
        return list(map(self.save, entities))


class AbstractMongoProjectEntityRepository(
    AbstractMongoNonProjectEntityRepository[T, MONGO_T]
):
    def find_by_project(self, domain_entity):
        # type: (KtrackId) -> List[T]
        mongo_entity = self.mongo_entity().objects(project__id=domain_entity).all()
        return list(map(self.to_domain_entity, mongo_entity))


class MongoProjectRepository(
    AbstractMongoNonProjectEntityRepository[Project, MongoProject], ProjectRepository
):
    def mongo_entity(self):
        # type: () -> Type[MongoProject]
        return MongoProject

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
                id=mongo_entity.id,
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
                id=mongo_entity.id,
                created_at=mongo_entity.created_at,
                updated_at=mongo_entity.updated_at,
                thumbnail=Thumbnail(path=mongo_entity.thumbnail.get("path")),
                name=mongo_entity.code,
                asset_type=mongo_entity.asset_type,
                project=mongo_entity.project["id"],
            )
