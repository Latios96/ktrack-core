import pytest
from mongoengine import connect, ValidationError

from ktrack_api.mongo_impl.entities import (
    Project as MongoProject,
    Asset as MongoAsset,
    PathEntry as MongoPathEntry,
)
from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
    MongoPathEntryRepository,
)
from kttk.domain.entities import Project, Thumbnail, Asset, PathEntry


@pytest.fixture
def mongo_project_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoProject.objects().all().delete()
    return MongoProjectRepository()


@pytest.fixture
def mongo_asset_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoAsset.objects().all().delete()
    return MongoAssetRepository()


@pytest.fixture
def mongo_path_entry_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoPathEntry.objects().all().delete()
    return MongoPathEntryRepository()


class BaseRepositoryTest(object):
    def _do_test_save(self, mongo_repository, domain_entity):
        old_entity = domain_entity
        assert not domain_entity.id

        domain_entity = mongo_repository.save(domain_entity)
        assert domain_entity.id

        old_entity.id = domain_entity.id
        assert old_entity == domain_entity
        assert mongo_repository.find_one(domain_entity.id) == domain_entity

    def _do_test_save_project_entity(
        self, mongo_repository, domain_entity, mongo_project_repository
    ):
        project = mongo_project_repository.save(Project(name="test_project"))
        domain_entity.project = project.id

        self._do_test_save(mongo_repository, domain_entity)

    def _do_test_save_all(self, mongo_repository, entities):
        old_projects = entities
        for p in entities:
            assert not p.id

        projects = mongo_repository.save_all(entities)
        assert len(projects) == len(old_projects)

        for project in projects:
            assert project.id
        assert mongo_repository.find_all() == projects

    def _do_test_save_all_project_entity(
        self, mongo_repository, entities, mongo_project_repository
    ):
        project = mongo_project_repository.save(Project(name="test_project"))
        for entity in entities:
            assert not entity.id
            entity.project = project.id

        self._do_test_save_all(mongo_repository, entities)


class TestProjectRepository(BaseRepositoryTest):
    @pytest.mark.parametrize(
        "project",
        [
            Project(name="test_project"),
            Project(name="test_project", thumbnail=Thumbnail(path="test")),
        ],
    )
    def test_save(self, project, mongo_project_repository):
        self._do_test_save(mongo_project_repository, project)

    def test_save_all(self, mongo_project_repository):
        projects = [
            Project(name="test_project"),
            Project(name="test_project", thumbnail=Thumbnail(path="test")),
        ]
        self._do_test_save_all(mongo_project_repository, projects)


class TestAssetRepository(BaseRepositoryTest):
    @pytest.mark.parametrize(
        "asset",
        [
            Asset(name="test_asset", asset_type="prop"),
            Asset(
                name="test_asset", asset_type="prop", thumbnail=Thumbnail(path="test")
            ),
        ],
    )
    def test_save(self, asset, mongo_asset_repository, mongo_project_repository):
        # type: (Asset, MongoAssetRepository, MongoProjectRepository) -> None
        self._do_test_save_project_entity(
            mongo_asset_repository, asset, mongo_project_repository
        )

    def test_save_all(self, mongo_asset_repository, mongo_project_repository):
        assets = [
            Asset(name="test_asset", asset_type="prop"),
            Asset(
                name="test_asset", asset_type="prop", thumbnail=Thumbnail(path="test")
            ),
        ]
        self._do_test_save_all_project_entity(
            mongo_asset_repository, assets, mongo_project_repository
        )

    def test_save_asset_without_project(self, mongo_asset_repository):
        asset = Asset(name="test_asset", asset_type="prop")

        with pytest.raises(ValidationError):
            mongo_asset_repository.save(asset)

    @pytest.mark.skip("asset type is not a required field yet!")
    def test_save_asset_without_asset_type(
        self, mongo_asset_repository, mongo_project_repository
    ):
        asset = Asset(name="test_asset")
        project = mongo_project_repository.save(Project(name="test_project"))
        asset.project = project.id

        with pytest.raises(ValidationError):
            mongo_asset_repository.save(asset)

    def test_find_by_project(self, mongo_project_repository, mongo_asset_repository):
        project1 = mongo_project_repository.save(Project(name="test_project"))
        project2 = mongo_project_repository.save(Project(name="test_project"))

        assets = mongo_asset_repository.save_all(
            [
                Asset(name="test_asset", asset_type="prop", project=project1.id),
                Asset(name="test_asset2", asset_type="prop", project=project2.id),
            ]
        )

        assert mongo_asset_repository.find_by_project(project1.id)[0] == assets[0]
        assert mongo_asset_repository.find_by_project(project2.id)[0] == assets[1]


class TestPathEntryRepository(BaseRepositoryTest):
    def test_save(self, mongo_path_entry_repository, populated_context):
        path_entry = PathEntry(path="some_path", context=populated_context)
        self._do_test_save(mongo_path_entry_repository, path_entry)

    def test_save_all(self, mongo_path_entry_repository, populated_context):
        path_entries = [
            PathEntry(path="some_path", context=populated_context),
            PathEntry(path="some_path", context=populated_context),
        ]
        self._do_test_save_all(mongo_path_entry_repository, path_entries)
