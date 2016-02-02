"""
Robot Framework from sublime is a autocompletion plugin for Sublime Text 3
"""
import sys
import os
import logging
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('Plugin only works with Sublime Text 3')

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


def plugin_loaded():
    pacake_folder = os.path.dirname(__name__)
