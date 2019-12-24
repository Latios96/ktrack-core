import pytest
from mongoengine import ValidationError

from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
)
from kttk.domain.entities import Project, Thumbnail, Asset, PathEntry


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

    def _do_test_delete(self, mongo_repository, entity):
        entity = mongo_repository.save(entity)
        assert entity.id

        mongo_repository.delete(entity.id)
        assert mongo_repository.find_one(entity.id) is None

    def _do_test_delete_project_entity(
        self, mongo_repository, entity, mongo_project_repository
    ):
        project = mongo_project_repository.save(Project(name="test_project"))
        entity.project = project.id
        entity = mongo_repository.save(entity)
        assert entity.id

        mongo_repository.delete(entity.id)
        assert mongo_repository.find_one(entity.id) is None


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

    def test_delete(self, mongo_project_repository):
        self._do_test_delete(mongo_project_repository, Project(name="test_project"))


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

    def test_find_by_project(self, mongo_asset_repository, mongo_project_repository):
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

    def test_delete(self, mongo_asset_repository, mongo_project_repository):
        asset = Asset(name="test_asset")
        self._do_test_delete_project_entity(
            mongo_asset_repository, asset, mongo_project_repository
        )


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

    def test_delete(self, mongo_path_entry_repository, populated_context):
        self._do_test_delete(
            mongo_path_entry_repository,
            PathEntry(path="some_path", context=populated_context),
        )

    def test_find_by_path(self, mongo_path_entry_repository, populated_context):
        path = "some_path"
        path_entry = PathEntry(path=path, context=populated_context)

        path_entry = mongo_path_entry_repository.save(path_entry)

        assert mongo_path_entry_repository.find_by_path(path) == path_entry

    def test_find_by_path_returns_none(
        self, mongo_path_entry_repository, populated_context
    ):
        path = "some_path"

        assert mongo_path_entry_repository.find_by_path(path) is None
