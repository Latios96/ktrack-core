import pytest
from tests.fixtures.ktrack_api_fixtures import (
    ktrack_instance,
    ktrack_instance_non_dropping,
    ktrack_instance_patched,
)
from tests.fixtures.context_fixtures import populated_context, fully_populated_context
from tests.fixtures.entity_fixtures import (
    project_dict,
    shot_dict,
    asset_dict,
    task_dict,
    workfile_dict,
    user_dict,
)
from tests.fixtures.integration_fixtures import (
    bootstrapped_project,
    bootstrapped_project_with_data,
)

from tests.fixtures.repository_fixtures import (
    mongo_project_repository,
    mongo_asset_repository,
    mongo_path_entry_repository,
    mongo_task_repository,
)


def pytest_addoption(parser):
    parser.addoption(
        "--integration-tests",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration-tests"):
        return
    skip_integration_tests_not_activated = pytest.mark.skip(
        reason="needs --integration-tests option to run"
    )
    for item in items:
        if "integration_test_only" in item.keywords:
            item.add_marker(skip_integration_tests_not_activated)
