import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from hashlib import md5
import json
from ..command_helper.current_view import CurrentView
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..setting.db_json_settings import DBJsonSetting


class ScanIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        log_file = get_setting(SettingObject.log_file)
        python_binary = get_setting(SettingObject.python_binary)
        table_dir = get_setting(SettingObject.table_dir)
        makedirs(path.dirname(log_file), exist_ok=True)
        self.view.run_command('scan')
        file_ = open(log_file, 'a')
        sublime.set_timeout_async(self.add_builtin_vars(table_dir))
        sublime.set_timeout_async(self.run_index(
                python_binary,
                table_dir,
                file_
            ), 0)
        file_.close()
        self.update_current_view_index()

    def run_index(self, python_binary, db_path, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
                [
                    python_binary,
                    get_setting(SettingObject.index_runner),
                    'all',
                    '--db_path',
                    db_path,
                    '--index_path',
                    get_setting(SettingObject.index_dir),
                    '--module_search_path',
                    get_setting(SettingObject.module_search_path)
                ],
                stderr=subprocess.STDOUT,
                stdout=log_file,
                startupinfo=startupinfo
            )
        rc = p.wait()
        if not rc == 0:
            print('See log file from database directory for details')
            raise ValueError(
                'Error in indexing, result code: {0}'.format(rc)
            )
        message = 'Indexing done with rc: {0}'.format(rc)
        sublime.status_message(message)
        print(message)

    def add_builtin_vars(self, db_path):
        builtin = 'BuiltIn'
        table_name = '{0}-{1}.json'.format(
            builtin, md5(builtin.encode('utf-8')).hexdigest())
        table_path = path.join(db_path, table_name)
        f_table = open(table_path, 'r')
        data = json.load(f_table)
        f_table.close()
        builtin_variables = get_setting(SettingObject.builtin_variables)
        data[DBJsonSetting.variables] = builtin_variables
        f_table = open(table_path, 'w')
        json.dump(data, f_table, indent=4)
        f_table.close()

    def update_current_view_index(self):
        file_name = self.view.file_name()
        if file_name:
            cv = CurrentView()
            workspace = get_setting(SettingObject.workspace)
            index_dir = get_setting(SettingObject.index_dir)
            extension = get_setting(SettingObject.extension)
            if cv.view_in_db(workspace, file_name, index_dir, extension):
                view_path = get_setting(SettingObject.view_path)
                cv.create_view(file_name, view_path, index_dir)
                message = 'Updating index is done for file: {0} '.format(
                    file_name
                )
                sublime.status_message(message)
                print(message)
