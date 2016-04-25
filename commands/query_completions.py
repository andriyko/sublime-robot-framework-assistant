import sublime_plugin
import sublime
from ..command_helper.completions import get_completion_list
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..setting.db_json_settings import DBJsonSetting
from ..command_helper.current_view import CurrentView
from ..command_helper.utils.get_text import get_line
from ..command_helper.utils.get_text import get_prefix
from ..command_helper.utils.get_text import get_object_from_line
from ..command_helper.get_metadata import get_rf_table_separator


class RobotCompletion(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        selection = view.sel()[0]
        scope_name = view.scope_name(selection.a).strip()
        if scope_name == DBJsonSetting.scope_name:
            if view.score_selector(selection.a - 1, 'comment'):
                return None
            elif view.score_selector(selection.a - 1, 'keyword.control.robot'):
                return None
            else:
                return self.return_completions(view, prefix, locations)
        else:
            return None

    def return_completions(self, view, prefix, locations):
        """Returns keyword and variable completions"""
        current_view = CurrentView()
        workspace = get_setting(SettingObject.workspace)
        open_tab = view.file_name()
        index_db = get_setting(SettingObject.index_dir)
        extension = get_setting(SettingObject.extension)
        view_in_db = current_view.view_in_db(workspace, open_tab,
                                             index_db, extension)
        view_completions = get_setting(
            SettingObject.view_completions)
        rc_cell = get_rf_table_separator(view)
        text_cursor_rigt = None
        line, column = get_line(view)
        if not prefix:
            data = get_prefix(line, column)
            prefix = data['match']
            text_cursor_rigt = data['rside']
        if view_in_db:
            object_name = get_object_from_line(line, prefix, column)
            arg_format = get_setting(SettingObject.arg_format)
            return get_completion_list(
                view_completions,
                prefix,
                text_cursor_rigt,
                rc_cell,
                object_name,
                arg_format
            )
        else:
            return None
