import pytest

from kttk.naming_system.naming_system import NamingSystem, NamingConfig
from kttk.naming_system.templates import PathTemplate


class TestFormatPathTemplate(object):
    @pytest.fixture(autouse=True)
    def setup_naming_system(self):
        config = NamingConfig(
            {
                PathTemplate(
                    name="my_template",
                    template_str="{test}",
                    expanded_template="{test}",
                ),
                PathTemplate(
                    name="my_template2",
                    template_str="{test1}{test2}",
                    expanded_template="{test1}{test2}",
                ),
            }
        )
        self._naming_system = NamingSystem(config)

    def test_no_path_template_with_name_found(self):
        naming_system = NamingSystem(NamingConfig(set()))

        with pytest.raises(KeyError):
            naming_system.format_path_template("any_name", {})

    def test_success(self):
        formatted_path_template = self._naming_system.format_path_template(
            "my_template", {"test": "my_str"}
        )
        assert formatted_path_template == "my_str"

    def test_missing_token(self):
        with pytest.raises(ValueError) as e:
            formatted_path_template = self._naming_system.format_path_template(
                "my_template", {"teste": "my_str"}
            )

        assert str(e.value) == "Some tokens are missing: test"

    def test_missing_multiple_tokens(self):
        with pytest.raises(ValueError) as e:
            formatted_path_template = self._naming_system.format_path_template(
                "my_template2", {"teste": "my_str"}
            )

        assert str(e.value) == "Some tokens are missing: test1, test2"
