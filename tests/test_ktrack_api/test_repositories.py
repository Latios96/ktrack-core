import pytest
from mongoengine import ValidationError

from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
    MongoTaskRepository,
    MongoWorkfileRepository,
)
from kttk.domain.entities import (
    Project,
    Thumbnail,
    Asset,
    PathEntry,
    KtrackId,
    EntityLink,
    Task,
    Shot,
    CutInformation,
    Workfile,
    VersionNumber,
)


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
            assert isinstance(project.id, KtrackId)
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

    def test_should_not_find_by_name(self, mongo_project_repository):
        assert not mongo_project_repository.find_by_name("")

    def test_should_find_by_name(self, mongo_project_repository):
        project = mongo_project_repository.save(Project(name="test_name"))

        assert mongo_project_repository.find_by_name("test_name") == project


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


class TestShotRepository(BaseRepositoryTest):
    @pytest.mark.parametrize(
        "shot",
        [
            Shot(
                code="sh010", cut_information=CutInformation(cut_in=1000, cut_out=1050)
            ),
            Shot(
                code="sh010", cut_information=CutInformation(cut_in=1010, cut_out=1040)
            ),
        ],
    )
    def test_save(self, shot, mongo_shot_repository, mongo_project_repository):
        # type: (Asset, MongoAssetRepository, MongoProjectRepository) -> None
        self._do_test_save_project_entity(
            mongo_shot_repository, shot, mongo_project_repository
        )

    def test_save_all(self, mongo_shot_repository, mongo_project_repository):
        shots = [
            Shot(
                code="sh010", cut_information=CutInformation(cut_in=1000, cut_out=1050)
            ),
            Shot(
                code="sh010", cut_information=CutInformation(cut_in=1010, cut_out=1040)
            ),
        ]
        self._do_test_save_all_project_entity(
            mongo_shot_repository, shots, mongo_project_repository
        )

    def test_save_shot_without_project(self, mongo_shot_repository):
        shot = Shot(
            code="sh010", cut_information=CutInformation(cut_in=1000, cut_out=1050)
        )

        with pytest.raises(ValidationError):
            mongo_shot_repository.save(shot)

    def test_find_by_project(self, mongo_shot_repository, mongo_project_repository):
        project1 = mongo_project_repository.save(Project(name="test_project"))
        project2 = mongo_project_repository.save(Project(name="test_project"))

        shots = mongo_shot_repository.save_all(
            [
                Shot(
                    code="sh010",
                    cut_information=CutInformation(cut_in=1000, cut_out=1050),
                    project=project1.id,
                ),
                Shot(
                    code="sh010",
                    cut_information=CutInformation(cut_in=1010, cut_out=1040),
                    project=project2.id,
                ),
            ]
        )

        assert mongo_shot_repository.find_by_project(project1.id)[0] == shots[0]
        assert mongo_shot_repository.find_by_project(project2.id)[0] == shots[1]

    def test_delete(self, mongo_shot_repository, mongo_project_repository):
        shot = Shot(
            code="sh010", cut_information=CutInformation(cut_in=1000, cut_out=1050)
        )
        self._do_test_delete_project_entity(
            mongo_shot_repository, shot, mongo_project_repository
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


class TestTaskRepository(BaseRepositoryTest):
    @pytest.mark.parametrize(
        "task",
        [
            Task(
                project="123",
                entity=EntityLink(type="asset", id="456"),
                name="task_name",
                step="lsr",
            ),
        ],
    )
    def test_save(self, task, mongo_task_repository, mongo_project_repository):
        # type: (Asset, MongoTaskRepository, MongoProjectRepository) -> None
        self._do_test_save_project_entity(
            mongo_task_repository, task, mongo_project_repository
        )

    def test_save_all(self, mongo_task_repository, mongo_project_repository):
        tasks = [
            Task(entity=EntityLink(type="asset", id="456"), name="lsr", step="lsr"),
            Task(
                entity=EntityLink(type="asset", id="456"), name="modelling", step="lsr"
            ),
        ]
        self._do_test_save_all_project_entity(
            mongo_task_repository, tasks, mongo_project_repository
        )

    def test_save_task_without_project(self, mongo_task_repository):
        task = Task(entity=EntityLink(type="asset", id="456"), name="lsr", step="lsr")

        with pytest.raises(ValidationError):
            mongo_task_repository.save(task)

    def test_find_by_project(self, mongo_task_repository, mongo_project_repository):
        project1 = mongo_project_repository.save(Project(name="test_project"))
        project2 = mongo_project_repository.save(Project(name="test_project"))

        tasks = mongo_task_repository.save_all(
            [
                Task(
                    entity=EntityLink(type="asset", id="456"),
                    name="lsr",
                    step="lsr",
                    project=project1.id,
                ),
                Task(
                    entity=EntityLink(type="asset", id="456"),
                    name="lsr",
                    step="lsr",
                    project=project2.id,
                ),
            ]
        )

        assert mongo_task_repository.find_by_project(project1.id)[0] == tasks[0]
        assert mongo_task_repository.find_by_project(project2.id)[0] == tasks[1]

    def test_delete(self, mongo_task_repository, mongo_project_repository):
        task = Task(entity=EntityLink(type="asset", id="456"), name="lsr", step="lsr")
        self._do_test_delete_project_entity(
            mongo_task_repository, task, mongo_project_repository
        )


class TestWorkfileRepository(BaseRepositoryTest):
    @pytest.mark.parametrize(
        "workfile",
        [
            Workfile(
                project="123",
                entity=EntityLink(type="asset", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            ),
        ],
    )
    def test_save(self, workfile, mongo_workfile_repository, mongo_project_repository):
        # type: (Workfile, MongoWorkfileRepository, MongoProjectRepository) -> None
        self._do_test_save_project_entity(
            mongo_workfile_repository, workfile, mongo_project_repository
        )

    def test_save_all(self, mongo_workfile_repository, mongo_project_repository):
        tasks = [
            Workfile(
                project="123",
                entity=EntityLink(type="asset", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            ),
            Workfile(
                project="123sdf",
                entity=EntityLink(type="asset", id="456"),
                name="taskydfg_name",
                path="test",
                comment="test",
                version_number=VersionNumber(3),
            ),
        ]
        self._do_test_save_all_project_entity(
            mongo_workfile_repository, tasks, mongo_project_repository
        )

    def test_save_task_without_project(self, mongo_workfile_repository):
        workfile = Workfile(
            entity=EntityLink(type="asset", id="456"),
            name="task_name",
            path="test",
            comment="test",
            version_number=VersionNumber(2),
        )

        with pytest.raises(ValidationError):
            mongo_workfile_repository.save(workfile)

    def test_find_by_project(self, mongo_workfile_repository, mongo_project_repository):
        project1 = mongo_project_repository.save(Project(name="test_project"))
        project2 = mongo_project_repository.save(Project(name="test_project"))

        workfiles = mongo_workfile_repository.save_all(
            [
                Workfile(
                    project=project1.id,
                    entity=EntityLink(type="asset", id="456"),
                    name="task_name",
                    path="test",
                    comment="test",
                    version_number=VersionNumber(2),
                ),
                Workfile(
                    project=project2.id,
                    entity=EntityLink(type="asset", id="456"),
                    name="taskydfg_name",
                    path="test",
                    comment="test",
                    version_number=VersionNumber(3),
                ),
            ]
        )

        assert mongo_workfile_repository.find_by_project(project1.id)[0] == workfiles[0]
        assert mongo_workfile_repository.find_by_project(project2.id)[0] == workfiles[1]

    def test_delete(self, mongo_workfile_repository, mongo_project_repository):
        task = Workfile(
            project="132",
            entity=EntityLink(type="asset", id="456"),
            name="task_name",
            path="test",
            comment="test",
            version_number=VersionNumber(2),
        )
        self._do_test_delete_project_entity(
            mongo_workfile_repository, task, mongo_project_repository
        )

    def test_find_by_version_number_not_existing_task_should_return_empty(
        self, mongo_workfile_repository
    ):
        assert not mongo_workfile_repository.find_by_task_and_version_number(
            "132", VersionNumber(1)
        )

    def test_find_by_version_number_should_return_empty(
        self, mongo_workfile_repository
    ):
        mongo_workfile_repository.save(
            Workfile(
                project="132",
                entity=EntityLink(type="task", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            )
        )

        assert not mongo_workfile_repository.find_by_task_and_version_number(
            "456", VersionNumber(1)
        )

    def test_find_by_version_number_should_return(self, mongo_workfile_repository):
        mongo_workfile_repository.save(
            Workfile(
                project="132",
                entity=EntityLink(type="task", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            )
        )

        assert mongo_workfile_repository.find_by_task_and_version_number(
            "456", VersionNumber(2)
        )

    def test_find_by_latest_not_existing_task_should_return_empty(
        self, mongo_workfile_repository
    ):
        assert not mongo_workfile_repository.find_by_task_latest("132")

    def test_find_by_latest_existing_task_should_return_empty(
        self, mongo_workfile_repository
    ):
        mongo_workfile_repository.save(
            Workfile(
                project="132",
                entity=EntityLink(type="task", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            )
        )
        assert not mongo_workfile_repository.find_by_task_latest("132")

    def test_find_by_latest_existing_task_should_return_latest(
        self, mongo_workfile_repository
    ):
        mongo_workfile_repository.save(
            Workfile(
                project="132",
                entity=EntityLink(type="task", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(2),
            )
        )
        mongo_workfile_repository.save(
            Workfile(
                project="132",
                entity=EntityLink(type="task", id="456"),
                name="task_name",
                path="test",
                comment="test",
                version_number=VersionNumber(1),
            )
        )
        workfile = mongo_workfile_repository.find_by_task_latest("456")
        assert workfile.version_number == VersionNumber(2)
