import attr
from enum import Enum


@attr.s(frozen=True)
class PathToken(object):
    name = attr.ib()  # type: str
    type = attr.ib()  # type: str # todo use enum
    regex = attr.ib()  # type: str


@attr.s(frozen=True)
class PathTemplate(object):
    name = attr.ib()  # type:str
    template_str = attr.ib()  # type:str
    expanded_template = attr.ib()  # type: str


FOLDER_SEPERATOR = PathToken("folder_seperator", "FOLDER_SEPERATOR", r"\/")
YEAR = PathToken("year", "STRING", r"\d{4}")
PROJECT_LOCATION = PathToken("project_location", "KNOWN_STRING", "M:/Projekte")
ASSET_TYPE = PathToken("project_drive", "STRING", ".*")

p = PathTemplate(
    "vrscene_location_asset", "{project_location}/{asset_type}", "M:/{asset_type}"
)
