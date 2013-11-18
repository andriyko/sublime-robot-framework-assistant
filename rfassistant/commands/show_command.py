#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import os

try:
    from rfassistant import settings_filename, no_manifest_file, no_libs_dir
except ImportError:
    from ...rfassistant import settings_filename, no_manifest_file, no_libs_dir


class RobotFrameworkShowManifestCommand(sublime_plugin.WindowCommand):
    s = None

    def run(self, *args, **kwargs):
        self.s = sublime.load_settings(settings_filename)
        libs_manifest = self.s.get('libs_manifest')
        if not os.path.exists(libs_manifest):
            return sublime.error_message(no_manifest_file(libs_manifest))
        self.window.open_file(libs_manifest)


class RobotFrameworkShowPackagesCommand(sublime_plugin.WindowCommand):
    s = None

    def run(self, *args, **kwargs):
        self.s = sublime.load_settings(settings_filename)
        libs_dir = self.s.get('libs_dir')
        if not os.path.exists(libs_dir):
            return sublime.error_message(no_libs_dir(libs_dir))
        self.window.run_command('open_dir', {"dir": libs_dir})
