from collections import Iterable

from typing import Optional

from ktrack_api.mongo_impl.entities import Project as MongoProject
from ktrack_api.repositories import ProjectRepository
from kttk.domain.entities import Project, Thumbnail


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
