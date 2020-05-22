import attr


@attr.s(frozen=True)
class PathTemplate(object):
    name = attr.ib()  # type:str
    template_str = attr.ib()  # type:str
