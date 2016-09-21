import sublime_plugin
import sublime
from os import path
from ..command_helper.completions import get_completion_list, check_prefix
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..setting.db_json_settings import DBJsonSetting
from ..dataparser.parser_utils.file_formatter import rf_table_name
from ..dataparser.parser_utils.util import get_index_name, normalise_path
from ..command_helper.utils.get_text import get_line
from ..command_helper.utils.get_text import get_object_from_line
from ..command_helper.get_metadata import get_rf_table_separator

SNIPPET_TRIGGER = [':f', '*', ':']


def get_index_file(open_tab):
    db_table = rf_table_name(normalise_path(open_tab))
    index_name = get_index_name(db_table)
    index_file = path.join(
        get_setting(SettingObject.index_dir),
        index_name
    )
    if not path.exists(index_file):
        index_file = None
    return index_file


class RobotCompletion(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        selection = view.sel()[0]
        scope_name = view.scope_name(selection.a).strip()
        if DBJsonSetting.scope_name in scope_name:
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
        # workspace = get_setting(SettingObject.workspace)
        open_tab = view.file_name()
        index_file = get_index_file(open_tab)
        if index_file:
            return self.get_completions(view, prefix, index_file)
        else:
            return None

    def get_completions(self, view, prefix, index_file):
        line, column = get_line(view)
        snippet = line[column - 2:column].strip()
        # To allow snippets to be triggered
        if snippet in SNIPPET_TRIGGER:
            return None
        new_prefix, new_column = check_prefix(line, column, prefix)
        rf_cell = get_rf_table_separator(view)
        object_name = get_object_from_line(line, prefix, column)
        arg_format = get_setting(SettingObject.arg_format)
        return get_completion_list(
            view_index=index_file,
            prefix=new_prefix,
            column=new_column,
            object_name=object_name,
            one_line=arg_format,
            rf_cell=rf_cell
        )
