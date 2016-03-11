import sublime_plugin
import sublime
import re
import time
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..command_helper.current_view import CurrentView
from ..command_helper.utils.get_text import get_line
from ..command_helper.noralize_cell import ReturnKeywordAndObject
from ..command_helper.get_metadata import get_rf_table_separator
from ..command_helper.get_keyword import GetKeyword


class JumpToKeyword(sublime_plugin.TextCommand):

    def run(self, edit):
        open_tab = self.view.file_name()
        db_dir = get_setting(SettingObject.table_dir)
        index_db = get_setting(SettingObject.index_dir)
        rf_cell = get_rf_table_separator(self.view)
        rf_extension = get_setting(SettingObject.extension)
        workspace = get_setting(SettingObject.workspace)
        current_view = CurrentView()
        view_in_db = current_view.view_in_db(workspace, open_tab,
                                             index_db, rf_extension)
        if view_in_db:
            line, column = get_line(self.view)
            view_completions = get_setting(SettingObject.view_completions)
            self.get_kw = ReturnKeywordAndObject(
                view_completions,
                rf_cell,
                rf_extension
            )
            keyword, object_name = self.get_kw.normalize(line, column)
            get_kw = GetKeyword(
                table_dir=db_dir,
                index_dir=index_db,
                open_tab=open_tab,
                rf_extension=rf_extension
            )
            regex, file_path = get_kw.return_file_and_patter(
                object_name=object_name,
                keyword=keyword
            )
            if file_path:
                self.go_to_kw(file_path, regex)
            else:
                sublime.status_message(
                    'Keyword: "{0}" is not found from db'.format(keyword)
                )
        else:
            sublime.status_message(
                'File: "{0}" is not found from db'.format(open_tab)
            )

    def go_to_kw(self, file_path, regex):
        window = sublime.active_window()
        new_view = window.open_file(file_path)
        while new_view.is_loading():
            time.sleep(0.2)
        text = new_view.substr(sublime.Region(0, new_view.size()))
        match = re.search(regex, text)
        region = sublime.Region(match.start(), match.end())
        new_view.show(region)
        new_view.sel().clear()
        new_view.sel().add(region)
