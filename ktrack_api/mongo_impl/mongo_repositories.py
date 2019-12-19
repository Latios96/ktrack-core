from collections import Iterable

from typing import Optional, List

from ktrack_api.mongo_impl.entities import Project as MongoProject, Asset as MongoAsset
from ktrack_api.repositories import ProjectRepository, AssetRepository
from kttk.domain.entities import Project, Thumbnail, Asset


class MongoProjectRepository(ProjectRepository[str]):

    @classmethod
    def to_mongo_project(cls, project):
        # type: (Project) -> MongoProject
        if project:
            return MongoProject(id=project.id,
                                created_at=project.created_at,
                                updated_at=project.updated_at,
                                thumbnail={'path': project.thumbnail.path} if project.thumbnail else {},
                                name=project.name)

    @classmethod
    def to_project(cls, mongo_project):
        # type: (MongoProject) -> Project
        if mongo_project:
            return Project(id=mongo_project.id,
                           created_at=mongo_project.created_at,
                           updated_at=mongo_project.updated_at,
                           thumbnail=Thumbnail(path=mongo_project.thumbnail.get('path')),
                           name=mongo_project.name)

    def find_one(self, the_id):
        # type: (str) -> Optional[Project]
        mongo_project = MongoProject.objects(id=the_id).first()
        return MongoProjectRepository.to_project(mongo_project)

    def find_all(self):
        # type: () -> Iterable[Project]
        return list(map(self.to_project, MongoProject.objects.all()))

    def save(self, entity):
        # type: (Project) -> Project
        mongo_project = MongoProjectRepository.to_mongo_project(entity)
        mongo_project.save()
        return MongoProjectRepository.to_project(mongo_project)

    def save_all(self, entities):
        # type: (Iterable[Project]) -> Iterable[Project]
        return list(map(self.save, entities))


class MongoAssetRepository(AssetRepository):

    @classmethod
    def to_mongo_entity(cls, domain_entity):
        # type: (Asset) -> MongoAsset
        if domain_entity:
            return MongoAsset(id=domain_entity.id,
                              created_at=domain_entity.created_at,
                              updated_at=domain_entity.updated_at,
                              thumbnail={'path': domain_entity.thumbnail.path} if domain_entity.thumbnail else {},
                              code=domain_entity.name,
                              asset_type=domain_entity.asset_type,
                              project={'type': 'project', 'id': domain_entity.project} if domain_entity.project else None)

    @classmethod
    def to_domain_entity(cls, mongo_entity):
        # type: (MongoAsset) -> Asset
        if mongo_entity:
            return Asset(id=mongo_entity.id,
                         created_at=mongo_entity.created_at,
                         updated_at=mongo_entity.updated_at,
                         thumbnail=Thumbnail(path=mongo_entity.thumbnail.get('path')),
                         name=mongo_entity.code,
                         asset_type=mongo_entity.asset_type,
                         project=mongo_entity.project['id'])

    def find_one(self, the_id):
        # type: (str) -> Optional[Asset]
        mongo_entity = MongoAsset.objects(id=the_id).first()
        return MongoAssetRepository.to_domain_entity(mongo_entity)

    def find_all(self):
        # type: () -> Iterable[Asset]
        return list(map(self.to_domain_entity, MongoAsset.objects.all()))

    def save(self, entity):
        # type: (Asset) -> Asset
        mongo_asset = MongoAssetRepository.to_mongo_entity(entity)
        mongo_asset.save()
        return MongoAssetRepository.to_domain_entity(mongo_asset)

    def save_all(self, entities):
        # type: (Iterable[Asset]) -> Iterable[Asset]
        return list(map(self.save, entities))

    def find_by_project(self, project):
        # type: (str) -> List[Asset]
        mongo_entity = MongoAsset.objects(project__id=project).all()
        return list(map(self.to_domain_entity, mongo_entity))
