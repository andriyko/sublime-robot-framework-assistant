import sublime_plugin
import sublime
import re
from os import path
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..command_helper.utils.get_text import get_line
from ..setting.db_json_settings import DBJsonSetting
from ..command_helper.workspace_objects import WorkSpaceObjects


class SettingImporter(sublime_plugin.TextCommand):

    def on_done(self, index):
        self.view.run_command(
            "insert_import",
            {'args': {'select': self.import_list[index], 'point': self.column}}
        )

    def import_type(self, line):
        resource = r'(?i)^(\| +)?resource ((\| )| +)$'
        library = r'(?i)^(\| +)?library ((\| )| +)$'
        variable = r'(?i)^(\| +)?variables ((\| )| +)$'
        if re.search(resource, line):
            return DBJsonSetting.resource_file
        elif re.search(library, line):
            return DBJsonSetting.library
        elif re.search(variable, line):
            return DBJsonSetting.variable_file
        else:
            return None

    def run(self, edit):
        line, column = get_line(self.view)
        db_dir = get_setting(SettingObject.table_dir)
        re_string = r'(?i)(^(\| +)?resource (\| )?)|(^(\| +)?library (\| )?)|(^(\| +)?variables (\| )?)'
        import_type = self.import_type(line)
        if re.search(re_string, line) and import_type:
            imports = WorkSpaceObjects(db_dir)
            self.import_list = imports.get_imports(import_type)
            window = self.view.window()
            self.column = self.view.sel()[0].begin()
            window.show_quick_panel(
                items=self.import_list,
                on_select=self.on_done
            )
        else:
            message = (
                'Cursor should have been in settings table '
                'Resource, Library or Variables import, but it was not'
            )
            sublime.status_message(message)


class InsertImport(sublime_plugin.TextCommand):
    def run(self, edit, args):
        file_name = args['select'][1]
        if path.exists(file_name):
            current_dir = path.dirname(self.view.file_name())
            file_name = path.relpath(file_name, current_dir)
            file_name = file_name.replace('\\', '/')
        self.view.insert(edit, args['point'], file_name)
