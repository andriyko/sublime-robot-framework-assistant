import sublime
import sublime_plugin

from ..setting.setting import get_log_file


class OpenLogFile(sublime_plugin.TextCommand):

    def run(self, edit):
        log_file = get_log_file()
        self.view.window().open_file(log_file)
