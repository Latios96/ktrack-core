import logging
import os

try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser

logger = logging.getLogger(__name__)


def read_connection_url():
    ini_path = os.path.join(os.path.dirname(__file__), "connection.ini")
    if os.path.exists(ini_path):
        config = configparser.ConfigParser()
        config.read(ini_path)
        return config.get("connection", "url")
    logger.warning("no connection.ini found, using mongomock for database connection!")
    return "mongomock://localhost"
