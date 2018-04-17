import re

import sublime_plugin
import sublime

from ..command_helper.get_keyword import GetKeyword
from ..command_helper.get_metadata import get_rf_table_separator
from ..command_helper.jump_to_file import JumpToFile
from ..command_helper.noralize_cell import ReturnKeywordAndObject
from ..command_helper.utils.get_text import get_line
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from .query_completions import get_index_file


class JumpToKeyword(sublime_plugin.TextCommand):

    def run(self, edit):
        open_tab = self.view.file_name()
        db_dir = get_setting(SettingObject.table_dir)
        index_db = get_setting(SettingObject.index_dir)
        rf_cell = get_rf_table_separator(self.view)
        rf_extension = get_setting(SettingObject.extension)
        index_file = get_index_file(open_tab)
        jump_to_file = JumpToFile()
        line, column = get_line(self.view)
        line = self.filter_given_when_then(line)
        if jump_to_file.is_import(line=line):
            imported = jump_to_file.get_import(line=line)
            file_path = jump_to_file.get_import_path(
                import_=imported,
                open_tab=open_tab,
                db_dir=db_dir
            )
            self.view.window().open_file(file_path)
        elif index_file:
            self.get_kw = ReturnKeywordAndObject(index_file, rf_cell)
            keyword, object_name = self.get_kw.normalize(line, column)
            if not keyword:
                message = ('Cursor location did not contain keyword '
                           'or keyword was not found from index.')
                sublime.status_message(message)
                return
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

    def filter_given_when_then(self, line):
        kw_prefixes = get_setting(SettingObject.kw_prefixes)
        if kw_prefixes:
            joined_kw_prefixes = "|".join(kw_prefixes)
            regex = r'(^| {4}|\t)(?i)(%s) (.*)$' % joined_kw_prefixes
            findings = re.search(regex, line)
            return findings.group(3) if findings else line
        else:
            return line

    def go_to_kw(self, file_path, regex):
        new_view = self.view.window().open_file(file_path)
        sublime.set_timeout(lambda: self.select_keyword(new_view, regex), 10)

    def select_keyword(self, new_view, regex):
        if not new_view.is_loading():
            text = new_view.substr(sublime.Region(0, new_view.size()))
            match = re.search(regex, text)
            region = sublime.Region(match.end(), match.start())
            new_view.sel().clear()
            new_view.sel().add(region)
            new_view.show(region)
        else:
            sublime.set_timeout(
                lambda: self.select_keyword(new_view, regex), 10)
