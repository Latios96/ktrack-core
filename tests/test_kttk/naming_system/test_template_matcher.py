import pytest

from kttk.naming_system.path_template_matcher import PathTokenMatcher
from kttk.naming_system.templates import PathToken

FOLDER_SEPERATOR = PathToken('folder_seperator', 'FOLDER_SEPERATOR', r'\/')
UNDERSCORE = PathToken('under_score', 'UNDERSCORE', r'_')
YEAR = PathToken('year', 'STRING', r'\d{4}')
PROJECT_DRIVE = PathToken('project_drive', 'KNOWN_STRING', 'M:')
PROJECTS_FOLDER = PathToken('projects_folder', 'KNOWN_STRING', 'Projekte')
ASSETS = PathToken('assets_folder', 'STRING', 'Assets')
ASSET_TYPE = PathToken('project_drive', 'STRING', 'Prop|Char|Environment')


class TestTemplateMatcher(object):

    @pytest.mark.parametrize("token_list,string", [
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR], 'M:/Projekte/2019'),
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR, ASSETS,
          FOLDER_SEPERATOR, ASSET_TYPE],
         'M:/Projekte/2018/Assets/Prop'),
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR, ASSETS,
          FOLDER_SEPERATOR, ASSET_TYPE],
         'M:/Projekte/2018/Assets/Char'),
    ])
    def test_should_match_template(self, token_list, string):
        matcher = PathTokenMatcher(token_list, string)

        assert matcher.matches()

    @pytest.mark.parametrize("token_list,string", [
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR], 'M:/Projekte/201'),
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR, ASSETS,
          FOLDER_SEPERATOR, ASSET_TYPE],
         'M:/Projekte/2018/Asets/Prop'),
        ([PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR, ASSETS,
          FOLDER_SEPERATOR, ASSET_TYPE],
         'M:/Projekte/2018/Assetss/Prop'),
    ])
    def test_should_not_match_template(self, token_list, string):
        matcher = PathTokenMatcher(token_list, string)

        assert not matcher.matches()

    def _test_should_match_template_debug(self):
        matcher = PathTokenMatcher([ASSETS],
                                   'Assetss')

        assert not matcher.matches()
