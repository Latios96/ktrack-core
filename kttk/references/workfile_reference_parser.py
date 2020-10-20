from kttk.references.workfile_reference import SerializedWorkfileReference


class WorkfileReferenceParser(object):
    def parse(self, string):
        # type: (str) -> SerializedWorkfileReference
        raise NotImplementedError()
