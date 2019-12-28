import pytest

from kttk.naming_system.naming_config import NamingConfig
from kttk.naming_system.naming_config_reader import (
    NamingConfigReader,
    RawConfigReader,
    RawConfig,
    RawConfigExpander,
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


class TestConfigExpander(object):
    @pytest.mark.parametrize(
        "raw_config,expected_naming_config",
        [
            (
                RawConfig(routes={"test": "test"}),
                NamingConfig(
                    path_templates={
                        PathTemplate(
                            name="test", template_str="test", expanded_template="test"
                        )
                    }
                ),
            ),
            (
                RawConfig(routes={"test": "{testing}"}),
                NamingConfig(
                    path_templates={
                        PathTemplate(
                            name="test",
                            template_str="{testing}",
                            expanded_template="{testing}",
                        )
                    }
                ),
            ),
            (
                RawConfig(routes={"test": "{testing}", "testing": "{wurst}"}),
                NamingConfig(
                    path_templates={
                        PathTemplate(
                            name="test",
                            template_str="{testing}",
                            expanded_template="{wurst}",
                        ),
                        PathTemplate(
                            name="testing",
                            template_str="{wurst}",
                            expanded_template="{wurst}",
                        ),
                    }
                ),
            ),
            (
                RawConfig(
                    routes={
                        "project_root": "M:/test/{project_name}",
                        "asset_root": "{project_root}/Assets",
                    }
                ),
                NamingConfig(
                    path_templates={
                        PathTemplate(
                            name="project_root",
                            template_str="M:/test/{project_name}",
                            expanded_template="M:/test/{project_name}",
                        ),
                        PathTemplate(
                            name="asset_root",
                            template_str="{project_root}/Assets",
                            expanded_template="M:/test/{project_name}/Assets",
                        ),
                    }
                ),
            ),
            (
                RawConfig(
                    routes={
                        "drive": "M:",
                        "projects_folder": "{drive}/Projekte/{project_year}",
                        "project_root": "{projects_folder}/{project_name}",
                        "asset_root": "{project_root}/Assets",
                        "asset_folder": "{asset_root}/{asset_type}/{asset_name}",
                    }
                ),
                NamingConfig(
                    path_templates={
                        PathTemplate(
                            name="drive", template_str="M:", expanded_template="M:",
                        ),
                        PathTemplate(
                            name="projects_folder",
                            template_str="{drive}/Projekte/{project_year}",
                            expanded_template="M:/Projekte/{project_year}",
                        ),
                        PathTemplate(
                            name="project_root",
                            template_str="{projects_folder}/{project_name}",
                            expanded_template="M:/Projekte/{project_year}/{project_name}",
                        ),
                        PathTemplate(
                            name="asset_root",
                            template_str="{project_root}/Assets",
                            expanded_template="M:/Projekte/{project_year}/{project_name}/Assets",
                        ),
                        PathTemplate(
                            name="asset_folder",
                            template_str="{asset_root}/{asset_type}/{asset_name}",
                            expanded_template="M:/Projekte/{project_year}/{project_name}/Assets/{asset_type}/{asset_name}",
                        ),
                    }
                ),
            ),
        ],
    )
    def test_expand_valid(self, raw_config, expected_naming_config):
        raw_config_expander = RawConfigExpander(raw_config)
        naming_config = raw_config_expander.expand()

        assert naming_config == expected_naming_config

    def test_expand_cyclic_recursion(self):
        raw_config = RawConfig(routes={"test": "{test}"})
        raw_config_expander = RawConfigExpander(raw_config)
        with pytest.raises(RuntimeError) as e:
            raw_config_expander.expand()


class TestReadConfig(object):
    def test_read(self):
        config_str = """
routes: 
    test: "{testr}"
"""
        config_reader = NamingConfigReader(config_str)
        naming_config = config_reader.read()

        expected_config = NamingConfig(
            {
                PathTemplate(
                    name="test", template_str="{testr}", expanded_template="{testr}"
                )
            }
        )

        assert naming_config == expected_config
