import pytest
from mongoengine import connect, ValidationError

from ktrack_api.mongo_impl.entities import Project as MongoProject, Asset as MongoAsset
from ktrack_api.mongo_impl.mongo_repositories import MongoProjectRepository, MongoAssetRepository
from kttk.domain.entities import Project, Thumbnail, Asset


@pytest.fixture
def mongo_project_repository():
    connect("mongoeengine_test",
            host='mongomock://localhost')
    MongoProject.objects().all().delete()
    return MongoProjectRepository()


@pytest.fixture
def mongo_asset_repository():
    connect("mongoeengine_test",
            host='mongomock://localhost')
    MongoAsset.objects().all().delete()
    return MongoAssetRepository()


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


class TestAssetRepository(object):

    @pytest.mark.parametrize("asset", [Asset(name='test_asset', asset_type='prop'),
                                       Asset(name='test_asset', asset_type='prop',
                                             thumbnail=Thumbnail(path='test'))])
    def test_save(self, asset, mongo_asset_repository, mongo_project_repository):
        # type: (Asset, MongoAssetRepository, MongoProjectRepository) -> None
        project = mongo_project_repository.save(Project(name='test_project'))
        asset.project = project.id

        old_asset = asset
        assert not asset.id

        asset = mongo_asset_repository.save(asset)
        assert asset.id
        old_asset.id = asset.id
        assert old_asset == asset

        assert mongo_asset_repository.find_one(asset.id) == asset

    def test_save_all(self, mongo_asset_repository, mongo_project_repository):
        project = mongo_project_repository.save(Project(name='test_project'))
        assets = [Asset(name='test_asset', asset_type='prop'),
                  Asset(name='test_asset', asset_type='prop',
                        thumbnail=Thumbnail(path='test'))]
        old_assets = assets

        for p in assets:
            assert not p.id
            p.project = project.id

        assets = mongo_asset_repository.save_all(assets)
        assert len(assets) == len(old_assets)

        for asset in assets:
            assert project.id

        assert mongo_asset_repository.find_all() == assets

    def test_save_asset_without_project(self, mongo_asset_repository):
        asset = Asset(name='test_asset', asset_type='prop')

        with pytest.raises(ValidationError):
            mongo_asset_repository.save(asset)

    @pytest.mark.skip("asset type is not a required field yet!")
    def test_save_asset_without_asset_type(self, mongo_asset_repository, mongo_project_repository):
        asset = Asset(name='test_asset')
        project = mongo_project_repository.save(Project(name='test_project'))
        asset.project = project.id

        with pytest.raises(ValidationError):
            mongo_asset_repository.save(asset)

    def test_find_by_project(self, mongo_project_repository, mongo_asset_repository):
        project1 = mongo_project_repository.save(Project(name='test_project'))
        project2 = mongo_project_repository.save(Project(name='test_project'))

        assets = mongo_asset_repository.save_all([Asset(name='test_asset', asset_type='prop', project=project1.id),
                                                  Asset(name='test_asset2', asset_type='prop', project=project2.id)])

        assert mongo_asset_repository.find_by_project(project1.id)[0] == assets[0]
        assert mongo_asset_repository.find_by_project(project2.id)[0] == assets[1]
