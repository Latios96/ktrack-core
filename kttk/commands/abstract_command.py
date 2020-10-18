from typing import List


class AbstractCommand(object):
    def __init__(self, stream):
        self._stream = stream

    def run(self, args):
        # type: (List[str]) -> None
        raise NotImplementedError()
