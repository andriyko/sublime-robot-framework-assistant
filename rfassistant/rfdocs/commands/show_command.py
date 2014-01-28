#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
import os

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ....rfassistant import PY2

if PY2:
    from rfassistant.settings import settings
    from rfassistant import no_manifest_file, no_libs_dir
else:
    from ....rfassistant.settings import settings
    from ....rfassistant import no_manifest_file, no_libs_dir


class RobotFrameworkShowManifestCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        rfdocs_manifest = settings.rfdocs_manifest
        if not os.path.exists(rfdocs_manifest):
            return sublime.error_message(no_manifest_file(rfdocs_manifest))
        self.window.open_file(rfdocs_manifest)


class RobotFrameworkShowPackagesCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        rfdocs_dir = settings.rfdocs_dir
        if not os.path.exists(rfdocs_dir):
            return sublime.error_message(no_libs_dir(rfdocs_dir))
        self.window.run_command('open_dir', {"dir": rfdocs_dir})
