import pytest
from mongoengine import connect

from ktrack_api.mongo_impl.entities import Project as MongoProject
from ktrack_api.mongo_impl.mongo_repositories import MongoProjectRepository
from kttk.domain.entities import Project, Thumbnail


@pytest.fixture
def mongo_project_repository():
    connect("mongoeengine_test",
            host='mongomock://localhost')
    MongoProject.objects().all().delete()
    return MongoProjectRepository()


class TestProjectRepository(object):

    @pytest.mark.parametrize("project", [Project(name='test_project'),
                                         Project(name='test_project', thumbnail=Thumbnail(path='test'))])
    def test_save(self, project, mongo_project_repository):
        old_project = project
        assert not project.id

        project = mongo_project_repository.save(project)
        assert project.id
        old_project.id = project.id
        assert old_project == project

        assert mongo_project_repository.find_one(project.id) == project

    def test_save_all(self, mongo_project_repository):
        projects = [Project(name='test_project'),
                    Project(name='test_project', thumbnail=Thumbnail(path='test'))]
        old_projects = projects

        for p in projects:
            assert not p.id

        projects = mongo_project_repository.save_all(projects)
        assert len(projects) == len(old_projects)

        for project in projects:
            assert project.id

        assert mongo_project_repository.find_all() == projects
