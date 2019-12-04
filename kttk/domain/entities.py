import datetime

import attr

KtrackId = str


@attr.s
class BasicEntity(object):
    id = attr.ib(type=KtrackId)
    created_at = attr.ib(type=datetime.datetime)
    updated_at = attr.ib(type=datetime.datetime)


@attr.s
class Thumbnail(BasicEntity):
    path = attr.ib(type=str)


@attr.s
class NonProjectEntity(BasicEntity):
    thumbnail = attr.ib(type=Thumbnail)


@attr.s
class Project(NonProjectEntity):
    name = attr.ib(type=str)


@attr.s
class ProjectEntity(NonProjectEntity):
    project = attr.ib(type=KtrackId)


@attr.s
class Asset(ProjectEntity):
    name = attr.ib(type=str)
    type = attr.ib(type=str)


@attr.s
class CutInformation(object):
    cut_in = attr.ib(type=int)
    cut_out = attr.ib(type=int)

    @property
    def cut_duration(self):
        # type: () -> int
        return self.cut_out - self.cut_in

    @property
    def frame_count(self):
        # type: () -> int
        return (self.cut_out - self.cut_in) + 1


@attr.s
class Shot(ProjectEntity):
    code = attr.ib(type=str)
    cut_information = attr.ib(type=CutInformation)


@attr.s
class EntityLink(object):
    type = attr.ib(type=str, converter=lambda x: x.lower())
    id = attr.ib(type=KtrackId)


@attr.s
class Task(ProjectEntity):
    name = attr.ib(type=str)
    step = attr.ib(type=str)
    entity = attr.ib(type=EntityLink)


def _parse_version_number(version_identifier):
    if not version_identifier:
        return version_identifier

    if isinstance(version_identifier, int):
        return version_identifier

    if version_identifier.startswith("v"):
        return int(version_identifier[1:])

    return int(version_identifier)


@attr.s
class VersionNumber(object):
    number = attr.ib(type=int, converter=_parse_version_number)

    @number.validator
    def check(self, attribute, value):
        if not value:
            raise ValueError("version number has to be > 0 and <= 999, was {}".format(value))
        if value <= 0 or value > 999:
            raise ValueError("version number has to be > 0 and <= 999, was {}".format(value))

    @property
    def version_str(self):
        return "v" + "{}".format(self.number).zfill(3)


@attr.s
class Workfile(ProjectEntity):
    name = attr.ib(type=str)
    entity = attr.ib(type=EntityLink)
    path = attr.ib(type=str)
    comment = attr.ib(type=str)
    version_number = attr.ib(type=VersionNumber)
    created_from = attr.ib(type=KtrackId)


class User(NonProjectEntity):
    name = attr.ib(type=str)
    first_name = attr.ib(type=str)
    second_name = attr.ib(type=str)
