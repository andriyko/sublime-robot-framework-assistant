import sublime_plugin
import sublime
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class OnSaveCreateTable(sublime_plugin.EventListener):
    """Enables automatic database table creation after file is saved"""

    def on_post_save_async(self, view):
        if get_setting(SettingObject.automatic_table_creation):
            view.run_command('scan_open_tab')
            if get_setting(SettingObject.automatic_index_creation):
                view.run_command('index_open_tab')
