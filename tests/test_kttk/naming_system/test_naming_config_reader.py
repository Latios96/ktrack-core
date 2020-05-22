import os

import pytest
import six

from kttk.naming_system.naming_config import NamingConfig
from kttk.naming_system.naming_config_reader import (
    NamingConfigReader,
    RawConfigReader,
    RawConfig,
    RouteTemplateExpander,
)
from kttk.naming_system.templates import PathTemplate, PathToken


class TestRawConfigReader(object):
    def test_read_simple(self):
        config_str = """
routes: 
    test: "{test}"
        """
        raw_config_reader = RawConfigReader(config_str)
        raw_config = raw_config_reader.read()

        assert raw_config == RawConfig(routes={"test": "{test}"},)

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
    tokens:
      - name: drive
        type: KNOWN_STRING
        regex: "M:"
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
            test: [test]
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
    test1:
        test2:
            asset:
                "{@wurst}"
    """,
            """
            
{   
    "routes": {
        "test1": {
            "test2": {
                "asset": "{@wurst}"
                    }
                }
        }
}
    """,
        ],
    )
    def test_read_valid(self, config_str):
        raw_config_reader = RawConfigReader(config_str)
        raw_config = raw_config_reader.read()

        assert raw_config == RawConfig(routes={"test1.test2.asset": "{@wurst}"})


class TestConfigExpander(object):
    @pytest.mark.parametrize(
        "raw_config,expected_naming_config",
        [
            (
                RawConfig(routes={"test": "test"}),
                NamingConfig(
                    path_templates={PathTemplate(name="test", template_str="test")}
                ),
            ),
            (
                RawConfig(routes={"test": "{testing}"}),
                NamingConfig(
                    path_templates={
                        PathTemplate(name="test", template_str="{testing}",)
                    }
                ),
            ),
            (
                RawConfig(routes={"test": "{testing}", "testing": "{wurst}"}),
                NamingConfig(
                    path_templates={
                        PathTemplate(name="test", template_str="{testing}",),
                        PathTemplate(name="testing", template_str="{wurst}",),
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
                            name="project_root", template_str="M:/test/{project_name}",
                        ),
                        PathTemplate(
                            name="asset_root", template_str="{project_root}/Assets",
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
                        PathTemplate(name="drive", template_str="M:"),
                        PathTemplate(
                            name="projects_folder",
                            template_str="{drive}/Projekte/{project_year}",
                        ),
                        PathTemplate(
                            name="project_root",
                            template_str="{projects_folder}/{project_name}",
                        ),
                        PathTemplate(
                            name="asset_root", template_str="{project_root}/Assets",
                        ),
                        PathTemplate(
                            name="asset_folder",
                            template_str="{asset_root}/{asset_type}/{asset_name}",
                        ),
                    }
                ),
            ),
        ],
    )
    def test_expand_valid(self, raw_config, expected_naming_config):
        raw_config_expander = RouteTemplateExpander(raw_config)
        naming_config = raw_config_expander.expand()

        assert naming_config == expected_naming_config


class TestReadConfig(object):
    expected_config = NamingConfig({PathTemplate(name="test", template_str="{testr}")})

    def test_read_str(self):
        config_str = """
tokens:
  - name: drive
    type: KNOWN_STRING
    regex: "M:"
routes: 
    test: "{testr}"
"""
        naming_config = NamingConfigReader.read_from_string(config_str)

        assert naming_config == self.expected_config

    def test_read_file(self):
        config_str = """
tokens:
  - name: drive
    type: KNOWN_STRING
    regex: "M:"
routes: 
    test: "{testr}"
"""
        naming_config = NamingConfigReader.read_from_file(six.StringIO(config_str))

        assert naming_config == self.expected_config

    def test_read_file_path(self):
        file_path = os.path.join(os.path.dirname(__file__), "simple_test_config.yml")
        naming_config = NamingConfigReader.read_from_file_path(file_path)

        assert naming_config == self.expected_config
