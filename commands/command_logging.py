import sublime_plugin
import sublime
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class LogCommands(sublime_plugin.TextCommand):

    def run(self, edit):
        """Enables and disabled Sublime API log_commands.

        Enable/disable is controlled by robot_framework_log_commands
        setting.

        For more details, see the Sublime API document:
        https://www.sublimetext.com/docs/3/api_reference.html
        """
        setting = get_setting(SettingObject.log_commands)
        if setting:
            sublime.log_commands(True)
            sublime.status_message('log_commands is enabled')
        else:
            sublime.log_commands(False)
            sublime.status_message('log_commands is disabled')
