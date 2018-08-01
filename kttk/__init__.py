__version__ = '0.2.0'

import logging

# create logger with 'spam_application'
logger = logging.getLogger('kttk')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
#fh = logging.FileHandler('kttk.log')
#fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
#logger.addHandler(fh)
logger.addHandler(ch)

from .folder_manager import init_entity
from .path_cache_manager import register_path, unregister_path, context_from_path
from .user_manager import restore_user, create_user, save_user_information
from .task_presets_manager import get_task_presets