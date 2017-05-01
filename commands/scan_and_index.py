import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from hashlib import md5
import json
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..setting.db_json_settings import DBJsonSetting


def index_popen_arg_parser(mode):
    arg_list = []
    arg_list.append(get_setting(SettingObject.python_binary))
    arg_list.append(get_setting(SettingObject.index_runner))
    arg_list.append(mode)
    arg_list.append('--db_path')
    arg_list.append(get_setting(SettingObject.table_dir))
    arg_list.append('--index_path')
    arg_list.append(get_setting(SettingObject.index_dir))
    arg_list.append('--path_to_lib_in_xml')
    arg_list.append(get_setting(SettingObject.lib_in_xml))
    arg_list.append('--module_search_path')
    for module in get_setting(SettingObject.module_search_path):
        arg_list.append(module)
    return arg_list


def add_builtin_vars(db_path):
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


class ScanIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        log_file = get_setting(SettingObject.log_file)
        db_dir = get_setting(SettingObject.table_dir)
        makedirs(path.dirname(log_file), exist_ok=True)
        self.view.run_command('scan')
        file_ = open(log_file, 'w')
        sublime.set_timeout_async(add_builtin_vars(db_dir))
        sublime.set_timeout_async(self.run_index(file_), 0)
        file_.close()

    def run_index(self, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
            index_popen_arg_parser('all'),
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
