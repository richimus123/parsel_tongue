# coding=utf-8
"""ParselTongue: Speak like a human, write like a Python.

    i.e. Natural Human Language translated into Python code.
"""

import logging
from logging.config import fileConfig

__version__ = '0.0.1'

fileConfig('logging_config.ini')
logger = logging.getLogger()
logger.debug('Initialized the module.')
