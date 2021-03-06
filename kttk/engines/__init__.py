from kttk import logger
from .abstract_engine import AbstractEngine
from typing import Type

g_current_engine = None


class NoEngineRunning(Exception):
    def __init__(self):
        super(NoEngineRunning, self).__init__("No engine is currently running!")


def current_engine():
    # type: () -> AbstractEngine
    """
    Returns the currently active engine.
    :returns: :class:`Engine` instance or None if no engine is running.
    """
    global g_current_engine
    return g_current_engine


def start_engine(engine_class):
    # type: (Type[AbstractEngine]) -> None
    global g_current_engine
    logger.info("starting engine {}..".format(engine_class.name))
    g_current_engine = engine_class()
    logger.info("engine {} started!".format(engine_class.name))
