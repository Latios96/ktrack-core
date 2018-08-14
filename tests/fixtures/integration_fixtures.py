import pytest

from kttk import project_bootstrapper


@pytest.fixture
def bootstrapped_project():
    # todo place project in some random path
    project, project_data = project_bootstrapper.bootstrap_project()
    yield project
    project_bootstrapper.remove_bootstrapped_project(project['id'])

@pytest.fixture
def bootstrapped_project_with_data():
    # todo place project in some random path
    project, project_data = project_bootstrapper.bootstrap_project()
    yield project, project_data
    project_bootstrapper.remove_bootstrapped_project(project['id'])