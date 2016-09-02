import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..dataparser.parser_utils.file_formatter import rf_table_name
from ..dataparser.parser_utils.util import normalise_path
from .scan_and_index import index_popen_arg_parser
from .scan_and_index import add_builtin_vars


class IndexOpenTabCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Command to index open tab RF file and create a index table.
        Purpose of the command is create index, from the open tab.
        Index should contain all the resource and library imports and
        all global variables from variable tables and imported variable
        files.
        """
        log_file = get_setting(SettingObject.log_file)
        makedirs(path.dirname(log_file), exist_ok=True)
        open_tab = self.view.file_name()
        if not open_tab:
            message = 'Not able to index because no tabs are active'
            sublime.status_message(message)
            return
        db_table_name = rf_table_name(normalise_path(open_tab))
        db_dir = get_setting(SettingObject.table_dir)
        sublime.set_timeout_async(add_builtin_vars(db_dir))
        if db_table_name:
            file_ = open(log_file, 'a')
            sublime.set_timeout_async(
                self.run_single_index(
                    db_table_name,
                    file_
                ),
                0
            )
            file_.close()
        else:
            message = 'Not able to index file: {0}'.format(open_tab)
            sublime.status_message(message)

    def run_single_index(self, db_table_name, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p_args = index_popen_arg_parser('single')
        p_args.append('--db_table')
        p_args.append(db_table_name)
        p = subprocess.Popen(
            p_args,
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
