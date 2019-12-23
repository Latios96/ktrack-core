from ktrack_faker import create_fake


def test_fake_asset():
    fake = create_fake()
    assert fake.asset()
    assert fake.asset().name
    assert fake.asset().type


def test_fake_asset_with_existing_movie():
    fake = create_fake()
    assert fake.asset(movie="Agent 327")
    assert fake.asset().name
    assert fake.asset().type


def test_fake_asset_with_non_existing_movie():
    fake = create_fake()
    assert fake.asset(movie="wurst")
    assert fake.asset().name
    assert fake.asset().type


def test_fake_movie():
    fake = create_fake()
    assert fake.movie()


def test_fake_shot_names():
    fake = create_fake()
    assert fake.shot_name()


def test_fake_project_names():
    fake = create_fake()
    assert fake.client_name()
    assert fake.project_name()
    assert fake.full_project_name()
