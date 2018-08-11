import pytest

from kttk import project_bootstrapper


@pytest.fixture
def bootstrapped_project():
    # todo place project in some random path
    project = project_bootstrapper.bootstrap_project()
    yield project
    project_bootstrapper.remove_bootstrapped_project(project['id'])