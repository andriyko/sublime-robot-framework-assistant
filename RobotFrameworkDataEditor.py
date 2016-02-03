"""
Robot Framework from sublime is a autocompletion plugin for Sublime Text 3
"""
import sys
import os
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('Plugin only works with Sublime Text 3')


def plugin_loaded():
    pacake_folder = os.path.dirname(__name__)
