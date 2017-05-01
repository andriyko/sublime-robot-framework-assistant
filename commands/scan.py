import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


def scan_popen_arg_parser(mode):
    arg_list = []
    arg_list.append(get_setting(SettingObject.python_binary))
    arg_list.append(get_setting(SettingObject.scanner_runner))
    arg_list.append(mode)
    arg_list.append('--db_path')
    arg_list.append(get_setting(SettingObject.table_dir))
    arg_list.append('--extension')
    arg_list.append(get_setting(SettingObject.extension))
    arg_list.append('--path_to_lib_in_xml')
    arg_list.append(get_setting(SettingObject.lib_in_xml))
    arg_list.append('--module_search_path')
    for module in get_setting(SettingObject.module_search_path):
        arg_list.append(module)
    return arg_list


class ScanCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Command to scan RF files and create database tables

        Purpose of the command is iterate over the files found from
        the robot_framework_workspace and create database tables.
        Also all imports, from found files, will be iterated and
        table is created also from imports.
        """
        log_file = get_setting(SettingObject.log_file)
        makedirs(path.dirname(log_file), exist_ok=True)
        file_ = open(log_file, 'a')
        sublime.set_timeout_async(self.run_scan(file_), 0)
        file_.close()

    def run_scan(self, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p_args = scan_popen_arg_parser('all')
        p_args.append('--workspace')
        p_args.append(get_setting(SettingObject.workspace))
        p = subprocess.Popen(
            p_args,
            stderr=subprocess.STDOUT,
            stdout=log_file,
            startupinfo=startupinfo
        )
        rc = p.wait()
        if rc != 0:
            print('See log file from database directory for details')
            raise ValueError('Error in scanning result code: {0}'.format(rc))
        message = 'Scaning done with rc: {0}'.format(rc)
        sublime.status_message(message)
        print(message)
