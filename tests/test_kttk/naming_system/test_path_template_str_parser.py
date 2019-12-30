import pytest

from kttk.naming_system.path_template_string_parser import (
    PathTemplateStringParser,
    ParsedPathToken,
)
from kttk.naming_system.templates import TokenType


class TestPathTemplateStringParser(object):
    @pytest.mark.parametrize(
        "str,expected_token_sequence",
        [
            ("{test}", [ParsedPathToken(type=TokenType.STRING, value="{test}")]),
            ("test", [ParsedPathToken(type=TokenType.KNOWN_STRING, value="test")]),
            ("/", [ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/")]),
            (
                "test/test",
                [
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="test"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="test"),
                ],
            ),
            (
                "{test}/test",
                [
                    ParsedPathToken(type=TokenType.STRING, value="{test}"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="test"),
                ],
            ),
            (
                "{project_root}/{project_name}/Shots/{code}/{code}_out/playblast",
                [
                    ParsedPathToken(type=TokenType.STRING, value="{project_root}"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.STRING, value="{project_name}"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="Shots"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.STRING, value="{code}"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.STRING, value="{code}"),
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="_out"),
                    ParsedPathToken(type=TokenType.FOLDER_SEPERATOR, value="/"),
                    ParsedPathToken(type=TokenType.KNOWN_STRING, value="playblast"),
                ],
            ),
        ],
    )
    def test_parse_correctly(self, str, expected_token_sequence):
        parser = PathTemplateStringParser(str)

        token_sequence = parser.parse()

        assert token_sequence == expected_token_sequence
