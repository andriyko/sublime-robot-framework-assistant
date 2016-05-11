import sublime_plugin
import sublime
from ..command_helper.update_current_view_json import update_current_view_index
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class DetectViewChange(sublime_plugin.EventListener):

    def on_activated(self, view):
        if get_setting(SettingObject.automatic_index_creation):
                view.run_command('index_open_tab')
        else:
            message = update_current_view_index(view)
            if message:
                sublime.status_message(message)
