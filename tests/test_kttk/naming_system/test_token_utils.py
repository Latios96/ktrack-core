import pytest

from kttk.naming_system.internal import token_utils


@pytest.mark.parametrize(
    "string,tokens",
    [
        ("", set()),
        ("{test}", {"test"}),
        ("{test", set()),
        ("test}", set()),
        ("{{test}}", {"test"}),
    ],
)
def test_find_all_tokens(string, tokens):
    assert token_utils.find_all_tokens(string) == tokens


@pytest.mark.parametrize(
    "string,token_dict,tokens",
    [
        ("", {}, set()),
        ("{test}", {}, {"test"}),
        ("{test}", {"test": "value"}, set()),
        (
            "M:/Projekte/{project_year}/{project_name}/Assets/{asset_type}/{asset_name}",
            {"test": "value"},
            {"project_year", "project_name", "asset_type", "asset_name"},
        ),
    ],
)
def test_get_missing_tokens(string, token_dict, tokens):
    assert token_utils.get_missing_tokens(string, token_dict) == tokens
