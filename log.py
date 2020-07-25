import logging

import dragonfly.log

SCRIPTS_LOGGER_NAME = 'scripts'

dragonfly.log.default_levels[SCRIPTS_LOGGER_NAME] = (logging.INFO, logging.INFO)
dragonfly.log.setup_log(use_stdout=True, use_file=False)
logger = logging.getLogger(SCRIPTS_LOGGER_NAME)

