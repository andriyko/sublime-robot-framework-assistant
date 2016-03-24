import sublime_plugin
import sublime
from ..command_helper.update_current_view_json import update_current_view_index


class DetectViewChange(sublime_plugin.EventListener):

    def on_activated(self, view):
        message = update_current_view_index(view)
        if message:
            sublime.status_message(message)
