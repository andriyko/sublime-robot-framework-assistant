import sublime_plugin
import sublime
from ..command_helper.current_view import CurrentView
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class DetectViewChange(sublime_plugin.EventListener):

    def on_activated(self, view):
        file_name = view.file_name()
        if file_name:
            cv = CurrentView()
            workspace = get_setting(SettingObject.workspace)
            index_dir = get_setting(SettingObject.index_dir)
            extension = get_setting(SettingObject.extension)
            file_name = view.file_name()
            if cv.view_in_db(workspace, file_name, index_dir, extension):
                view_path = get_setting(SettingObject.view_path)
                cv.create_view(file_name, view_path, index_dir)
