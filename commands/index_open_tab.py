import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..dataparser.parser_utils.file_formatter import rf_table_name
from ..dataparser.parser_utils.util import normalise_path
from ..command_helper.update_current_view_json import update_current_view_index


class IndexOpenTabCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Command to index open tab RF file and create db index table.

        Purpose of the command is create index, from the open tab.
        Index should contain all the resource and library imports and
        all global variables from variable tables and imported variable
        files.
        """
        log_file = get_setting(SettingObject.log_file)
        python_binary = get_setting(SettingObject.python_binary)
        table_dir = get_setting(SettingObject.table_dir)
        makedirs(path.dirname(log_file), exist_ok=True)
        open_tab = self.view.file_name()
        if not open_tab:
            message = 'Not able to index because no tabs are active'
            sublime.status_message(message)
            return
        db_table_name = self.get_table_name(open_tab)
        if db_table_name:
            file_ = open(log_file, 'a')
            sublime.set_timeout_async(self.run_single_index(
                    python_binary,
                    table_dir,
                    db_table_name,
                    file_
                ), 0)
            file_.close()
            message = update_current_view_index(self.view)
            sublime.status_message(message)
        else:
            message = 'Not able to index file: {0}'.format(open_tab)
            sublime.status_message(message)

    def run_single_index(self, python_binary, db_path, db_table, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
                [
                    python_binary,
                    get_setting(SettingObject.index_runner),
                    'single',
                    '--db_path',
                    db_path,
                    '--db_table',
                    db_table,
                    '--index_path',
                    get_setting(SettingObject.index_dir),
                    '--module_search_path',
                    get_setting(SettingObject.module_search_path),
                    '--path_to_lib_in_xml',
                    get_setting(SettingObject.lib_in_xml)
                ],
                stderr=subprocess.STDOUT,
                stdout=log_file,
                startupinfo=startupinfo
            )
        rc = p.wait()
        if not rc == 0:
            print('See log file from database directory for details')
            message = 'Error in indexing, result code: {0}'.format(rc)
            sublime.status_message(message)
            raise ValueError(message)
        message = 'Indexing done with rc: {0}'.format(rc)
        sublime.status_message(message)
        print(message)

    def get_table_name(self, open_tab):
        workspace = get_setting(SettingObject.workspace)
        workspace_norm = path.normcase(workspace)
        open_tab_norm = path.normcase(open_tab)
        extension = get_setting(SettingObject.extension)
        if open_tab_norm.endswith(extension):
            if open_tab_norm.startswith(workspace_norm):
                return rf_table_name(normalise_path(open_tab))
        else:
            return False
