import pytest

from kttk.naming_system.path_token_matcher import PathTokenSequenceMatcher
from kttk.naming_system.templates import PathToken

FOLDER_SEPERATOR = PathToken('folder_seperator', 'FOLDER_SEPERATOR', r'\/')
YEAR = PathToken('year', 'STRING', r'\d{4}')
PROJECT_DRIVE = PathToken('project_drive', 'KNOWN_STRING', 'M:')
PROJECTS_FOLDER = PathToken('projects_folder', 'KNOWN_STRING', 'Projekte')
PROJECT_NAME = PathToken('projects_name', 'STRING', '.*')
ARCHIVE = PathToken('archive', 'KNOWN_STRING', '_archive')
ASSETS = PathToken('assets_folder', 'STRING', 'Assets')
ASSET_TYPE = PathToken('project_drive', 'STRING', 'Prop|Char|Environment')


class TestTemplateMatcher(object):
    PROJECT_LOCATION = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR]

    ASSET_TYPE_FOLDER = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR,
                         PROJECT_NAME,
                         FOLDER_SEPERATOR, ASSETS,
                         FOLDER_SEPERATOR, ASSET_TYPE]

    COMBINED_PLACEHOLDERS = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECT_NAME, FOLDER_SEPERATOR, PROJECT_NAME, ARCHIVE]

    @pytest.mark.parametrize("token_list,string", [
        (PROJECT_LOCATION, 'M:/Projekte/2019'),
        (ASSET_TYPE_FOLDER, 'M:/Projekte/2018/test/Assets/Prop'),
        (ASSET_TYPE_FOLDER, 'M:/Projekte/2018/test/Assets/Char'),
        (COMBINED_PLACEHOLDERS, 'M:/test/test_archive')
    ])
    def test_should_match_template(self, token_list, string):
        matcher = PathTokenSequenceMatcher(token_list, string)

        assert matcher.matches()

    @pytest.mark.parametrize("token_list,string", [
        (PROJECT_LOCATION, 'M:/Projekte/201'),
        (ASSET_TYPE_FOLDER,
         'M:/Projekte/2018/test/Asets/Prop'),
        (ASSET_TYPE_FOLDER,
         'M:/Projekte/2018/test/Assetss/Prop'),
        (COMBINED_PLACEHOLDERS, 'M:/test/tests_archive'),
        (COMBINED_PLACEHOLDERS, 'M:/test/tesst_archive'),
        (COMBINED_PLACEHOLDERS, 'M:/tesst/test_archive'),
    ])
    def test_should_not_match_template(self, token_list, string):
        matcher = PathTokenSequenceMatcher(token_list, string)

        assert not matcher.matches()

    def _test_should_match_template_debug(self):
        matcher = PathTokenSequenceMatcher(self.COMBINED_PLACEHOLDERS, 'M:/test/tests_archive')

        assert matcher.matches()
