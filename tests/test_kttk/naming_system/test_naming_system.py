import pytest

from kttk.naming_system.naming_system import NamingSystem
from kttk.naming_system.internal.naming_config import NamingConfig
from kttk.naming_system.internal.templates import PathTemplate


class TestFormatPathTemplate(object):
    @pytest.fixture(autouse=True)
    def setup_naming_system(self):
        config = NamingConfig(
            {
                PathTemplate(name="my_template", template_str="{test}"),
                PathTemplate(name="my_template_with_dots", template_str="{test.teste}"),
                PathTemplate(name="my_template2", template_str="{test1}{test2}"),
                PathTemplate(name="my_template3", template_str="{@my_template}"),
                PathTemplate(name="my_template4", template_str="{@my_template2}"),
                PathTemplate(
                    name="defaultTokens",
                    template_str="{current_date.year}{platform.name}{current_date.hour}{current_date.minute}{current_date.second}{current_user.name}",
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

    def test_missing_token_referenced(self):
        with pytest.raises(ValueError) as e:
            formatted_path_template = self._naming_system.format_path_template(
                "my_template3", {"teste": "my_str"}
            )

        assert str(e.value) == "Some tokens are missing: test"

    def test_missing_multiple_tokens(self):
        with pytest.raises(ValueError) as e:
            formatted_path_template = self._naming_system.format_path_template(
                "my_template2", {"teste": "my_str"}
            )

        assert str(e.value) == "Some tokens are missing: test1, test2"

    def test_missing_multiple_tokens_referenced(self):
        with pytest.raises(ValueError) as e:
            formatted_path_template = self._naming_system.format_path_template(
                "my_template4", {"teste": "my_str"}
            )

        assert str(e.value) == "Some tokens are missing: test1, test2"

    def test_default_tokens_no_context_provided(self):
        formated_template = self._naming_system.format_path_template(
            "defaultTokens", {}
        )

        for token in ["year", "platform", "hour", "minute", "second", "user"]:
            assert token not in formated_template
