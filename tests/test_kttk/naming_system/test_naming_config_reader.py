import pytest

from kttk.naming_system.naming_config import NamingConfig
from kttk.naming_system.naming_config_reader import (
    NamingConfigReader,
    RawConfigReader,
    RawConfig,
)
from kttk.naming_system.templates import PathTemplate


# todo check for cyclic expansion
# todo check for impossible expansion
# todo check for invalid path templates (some which can not be properly parsed afterwards)


class TestRawConfigReader(object):
    def test_read_simple(self):
        config_str = """
        routes: 
            test: "{test}"
        """
        raw_config_reader = RawConfigReader(config_str)
        raw_config = raw_config_reader.read()

        assert raw_config == RawConfig(routes={"test": "{test}"})

    @pytest.mark.parametrize(
        "config_str,message",
        [
            (
                """
""",
                "could not load data from given string!",
            ),
            (
                """
test: test
""",
                '"routes" key missing in config!',
            ),
            (
                """
routes: []
""",
                "routes section is not a dictionary!",
            ),
            (
                """
routes: test
""",
                "routes section is not a dictionary!",
            ),
            (
                """
routes: 1
""",
                "routes section is not a dictionary!",
            ),
            (
                """
routes: 2.0
""",
                "routes section is not a dictionary!",
            ),
            (
                """
routes:
    test: [test]
""",
                "route is not a string-string mapping!",
            ),
            (
                """
routes:
    test:
        test: test
""",
                "route is not a string-string mapping!",
            ),
        ],
    )
    def test_read_invalid(self, config_str, message):
        raw_config_reader = RawConfigReader(config_str)
        with pytest.raises(ValueError) as e:
            raw_config = raw_config_reader.read()

        assert str(e.value) == message

    @pytest.mark.parametrize(
        "config_str",
        [
            """
routes:
    test: test
    """,
            """
{
    "routes": {
        "test": "test"
        }
}
    """,
        ],
    )
    def test_read_valid(self, config_str):
        raw_config_reader = RawConfigReader(config_str)
        raw_config = raw_config_reader.read()

        assert raw_config == RawConfig(routes={"test": "test"})


class TestReadConfig(object):
    def test_read(self):
        config_str = """
routes: 
    test: "{test}"
"""
        config_reader = NamingConfigReader(config_str)
        naming_config = config_reader.read()

        expected_config = NamingConfig(
            {
                PathTemplate(
                    name="test", template_str="{test}", expanded_template="{test}"
                )
            }
        )

        assert naming_config == expected_config
