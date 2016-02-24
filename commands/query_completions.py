import sublime_plugin
import sublime
from ..command_helper.completions import get_completion_list
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..command_helper.current_view import CurrentView
from ..command_helper.get_text import get_line
from ..command_helper.get_text import get_prefix


class RobotCompletion(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        current_view = CurrentView()
        workspace = get_setting(SettingObject.workspace)
        open_tab = view.file_name()
        index_db = get_setting(SettingObject.index_dir)
        extension = get_setting(SettingObject.extension)
        view_in_db = current_view.view_in_db(workspace, open_tab,
                                             index_db, extension)
        view_completions = get_setting(
            SettingObject.view_completions)
        if not prefix:
            column, line = get_line(view)
            prefix = get_prefix(line, column)
        if view_in_db:
            return get_completion_list(view_completions, prefix)
        else:
            return None
