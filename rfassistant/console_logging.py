#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Sublime imports
import sublime

# Python imports
import functools
import logging
import traceback

# Plugin imports
try:
    from rfassistant.settings import settings
except ImportError:
    from .settings import settings


class Logger:
    """
    Sublime Console Logger.
    """
    def __init__(self, name):
        self.name = str(name)

    @property
    def level(self):
        level = settings.log_level
        return getattr(logging, level.upper())

    def _print(self, msg):
        print(': '.join([self.name, str(msg)]))

    def log(self, level, msg, **kwargs):
        """
        Thread-safe logging
        """
        log = functools.partial(self._log, level, msg, **kwargs)
        sublime.set_timeout(log, 0)

    def _log(self, level, msg, **kwargs):
        if self.level <= level:
            self._print(msg)
            if level == logging.ERROR and kwargs.get('exc_info'):
                traceback.print_exc()

    def debug(self, msg):
        self.log(logging.DEBUG, msg)

    def info(self, msg):
        self.log(logging.INFO, msg)

    def error(self, msg, exc_info=False):
        self.log(logging.ERROR, msg, exc_info=exc_info)

    def exception(self, msg):
        self.error(msg, exc_info=True)

    def warning(self, msg):
        self.log(logging.WARN, msg)


getLogger = Logger