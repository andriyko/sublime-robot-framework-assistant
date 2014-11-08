#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
import json
import subprocess
import os
# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ...rfassistant import PY2

if PY2:
    from rfassistant import console_logging as logging
    from rfassistant import package_dir, no_python_interpreter
    from rfassistant.settings import settings
else:
    from ...rfassistant import console_logging as logging
    from ...rfassistant import package_dir, no_python_interpreter
    from ..settings import settings

logger = logging.getLogger(__name__)


def get_settings_dict():
    # return json.dumps(settings.to_dict())
    return settings.to_dict()


def get_python_interpreter(s):
    python_interpreter = s.python_interpreter
    if not os.path.exists(python_interpreter):
        sublime.error_message(no_python_interpreter(python_interpreter))
        return
    return python_interpreter


class RobotFrameworkScanPythonLibsCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        python_interpreter = get_python_interpreter(settings)
        if not python_interpreter:
            return
        scanner_config = settings.scanner_config
        python_libs_dir_path = settings.python_libs_dir

        logger.debug('Python interpreter: {0}'.format(python_interpreter))
        process = subprocess.Popen(
            [python_interpreter, '-m', 'rfassistant.run_scanners', 'pylib',
             scanner_config, python_libs_dir_path, json.dumps(get_settings_dict())],
            cwd=r'%s' % package_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()
        logger.debug(stdout)
        logger.error(stderr)


class RobotFrameworkScanResourceFilesCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        python_interpreter = get_python_interpreter(settings)
        if not python_interpreter:
            return
        scanner_config = settings.scanner_config
        resources_dir = settings.resources_dir

        logger.debug('Python interpreter: {0}'.format(python_interpreter))
        process = subprocess.Popen(
            [python_interpreter, '-m', 'rfassistant.run_scanners', 'resource',
             scanner_config, resources_dir, json.dumps(get_settings_dict())],
            cwd=r'%s' % package_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()
        logger.debug(stdout)
        logger.error(stderr)


class RobotFrameworkScanPythonLibsAndResourceFilesCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        python_interpreter = get_python_interpreter(settings)
        if not python_interpreter:
            return
        scanner_config = settings.scanner_config
        resources_dir = settings.resources_dir
        python_libs_dir_path = settings.python_libs_dir

        logger.debug('Python interpreter: {0}'.format(python_interpreter))

        process = subprocess.Popen(
            [python_interpreter, '-m', 'rfassistant.run_scanners', 'pylib',
             scanner_config, python_libs_dir_path, json.dumps(get_settings_dict())],
            cwd=r'%s' % package_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        logger.debug(stdout)
        logger.error(stderr)

        process = subprocess.Popen(
            [python_interpreter, '-m', 'rfassistant.run_scanners', 'resource',
             scanner_config, resources_dir, json.dumps(get_settings_dict())],
            cwd=r'%s' % package_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        logger.debug(stdout)
        logger.error(stderr)


class RobotFrameworkScanTestCaseFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_to_read):
        python_interpreter = get_python_interpreter(settings)
        if not python_interpreter:
            return
        scanner_config = settings.scanner_config

        logger.debug('Python interpreter: {0}'.format(python_interpreter))
        process = subprocess.Popen(
            [python_interpreter, '-m', 'rfassistant.run_scanners', 'testcase',
             scanner_config, file_to_read, json.dumps(get_settings_dict())],
            cwd=r'%s' % package_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()
        logger.debug(stdout)
        logger.error(stderr)
