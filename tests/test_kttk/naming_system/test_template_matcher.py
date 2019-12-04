import pytest

from kttk.naming_system.path_token_matcher import PathTokenSequenceMatcher
from kttk.naming_system.templates import PathToken

FOLDER_SEPERATOR = PathToken('folder_seperator', 'FOLDER_SEPERATOR', r'\/')
UNDERSCORE = PathToken('underscore', 'UNDERSCORE', r'_')
YEAR = PathToken('year', 'STRING', r'\d{4}')
PROJECT_DRIVE = PathToken('project_drive', 'KNOWN_STRING', 'M:')
PROJECTS_FOLDER = PathToken('projects_folder', 'KNOWN_STRING', 'Projekte')
PROJECT_NAME = PathToken('project_name', 'STRING', '.*')
ARCHIVE = PathToken('archive', 'KNOWN_STRING', '_archive')
ASSETS = PathToken('assets_folder', 'STRING', 'Assets')
ASSET_TYPE = PathToken('asset_type', 'STRING', 'Prop|Char|Environment')
EXTENSION = PathToken('extension', 'STRING', '.*')

VERSION = PathToken('version_number', 'STRING', 'v\d{3}')


class TestTemplateMatcher(object):
    PROJECT_LOCATION = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR]

    ASSET_TYPE_FOLDER = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECTS_FOLDER, FOLDER_SEPERATOR, YEAR, FOLDER_SEPERATOR,
                         PROJECT_NAME,
                         FOLDER_SEPERATOR, ASSETS,
                         FOLDER_SEPERATOR, ASSET_TYPE]

    COMBINED_PLACEHOLDERS = [PROJECT_DRIVE, FOLDER_SEPERATOR, PROJECT_NAME, FOLDER_SEPERATOR, PROJECT_NAME, ARCHIVE]

    PROJECT_NAME_WITH_UNDERSCORE = [PROJECT_NAME, FOLDER_SEPERATOR, PROJECT_NAME, UNDERSCORE, ASSET_TYPE, UNDERSCORE,
                                    VERSION, EXTENSION]

    @pytest.mark.parametrize("token_list,string", [
        (PROJECT_LOCATION, 'M:/Projekte/2019'),
        (ASSET_TYPE_FOLDER, 'M:/Projekte/2018/test/Assets/Prop'),
        (ASSET_TYPE_FOLDER, 'M:/Projekte/2018/test/Assets/Char'),
        (COMBINED_PLACEHOLDERS, 'M:/test/test_archive'),
        (PROJECT_NAME_WITH_UNDERSCORE, 'test_ing/test_ing_Prop_v001.mb')
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

    @pytest.mark.parametrize("token_list,string,values", [
        (PROJECT_LOCATION, 'M:/Projekte/2019',
         {'project_drive': 'M:', 'folder_seperator': '/', 'projects_folder': 'Projekte', 'year': '2019'}),
        (COMBINED_PLACEHOLDERS, 'M:/test/test_archive',
         {'project_drive': 'M:', 'folder_seperator': '/', 'project_name': 'test', 'archive': '_archive'}),
        (PROJECT_NAME_WITH_UNDERSCORE, 'test_ing/test_ing_Prop_v001.mb',
         {'project_name': 'test_ing', 'folder_seperator': '/', 'asset_type': 'Prop', 'underscore': '_',
          'version_number': 'v001', 'extension': '.mb', })
    ])
    def test_should_return_correct_values(self, token_list, string, values):
        matcher = PathTokenSequenceMatcher(token_list, string)

        assert matcher.matches() == values

    def _test_should_match_template_debug(self):
        matcher = PathTokenSequenceMatcher(self.PROJECT_NAME_WITH_UNDERSCORE, 'test_ing/test_ing_Prop_v001.mb')

        assert matcher.matches()
