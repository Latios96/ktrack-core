import os

import pytest


def integration_tests_enabled():
    # type: () -> bool
    """
    Returns True if integration tests re enabled using enviroment variable
    :return: True if avaible, False otherwise
    """
    return "KTRACK_ENABLE_INTEGRATION_TESTS" in os.environ.keys()


integration_test_only = pytest.mark.skipif(
    not integration_tests_enabled(), reason="Integration tests disabled"
)
