from ktrack_faker import create_fake


class TestFaker(object):
    def setup_method(self):
        self.fake = create_fake()

    def test_fake_asset(self):
        assert self.fake.asset()
        assert self.fake.asset().name
        assert self.fake.asset().type

    def test_fake_asset_with_existing_movie(self):
        for i in range(20):
            assert self.fake.asset(movie="Agent 327")
            assert self.fake.asset().name
            assert self.fake.asset().type

    def test_fake_asset_with_non_existing_movie(self):
        assert self.fake.asset(movie="wurst")
        assert self.fake.asset().name
        assert self.fake.asset().type

    def test_fake_movie(self):
        for i in range(10):
            assert self.fake.movie()

    def test_fake_shot_names(self):
        assert self.fake.shot_name()

    def test_fake_project_names(self):
        for i in range(50):
            assert self.fake.client_name()
            assert self.fake.project_name()
            assert self.fake.full_project_name()
