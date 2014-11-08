#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ..rfassistant import PY2

if PY2:
    from rfassistant.settings import settings
    from rfassistant import robot_tm_language_path
    from mixins import is_robot_or_txt_file
else:
    from .settings import settings
    from ..rfassistant import robot_tm_language_path
    from .mixins import is_robot_language_file

views_to_center = {}
detect_robot_regex = '\*+\s*(settings?|metadata|(user )?keywords?|test ?cases?|variables?)'


class AutoSyntaxHighlight(sublime_plugin.EventListener):
    def autodetect(self, view):
        view_file_name = view.file_name()
        if all([view_file_name is not None,
                is_robot_language_file(view_file_name, settings.associated_file_extensions),
                view.find(detect_robot_regex, 0, sublime.IGNORECASE) is not None]):
            view.set_syntax_file(robot_tm_language_path)

    def on_load(self, view):
        if view.id() in views_to_center:
            view.show_at_center(view.text_point(views_to_center[view.id()], 0))
            del views_to_center[view.id()]
        self.autodetect(view)

    def on_post_save(self, view):
        self.autodetect(view)