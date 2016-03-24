import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class ScanCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Command to scan RF files and create database tables

        Purpose of the command is iterate over the files found from
        the robot_framework_workspace and create database tables.
        Also all imports, from found files, will be iterated and
        table is created also from imports.
        """
        log_file = get_setting(SettingObject.log_file)
        python_binary = get_setting(SettingObject.python_binary)
        table_dir = get_setting(SettingObject.table_dir)
        makedirs(path.dirname(log_file), exist_ok=True)
        file_ = open(log_file, 'w')
        sublime.set_timeout_async(self.run_scan(
                python_binary,
                table_dir,
                file_
            ), 0)
        file_.close()

    def run_scan(self, python_binary, db_path, log_file):
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
                [
                    python_binary,
                    get_setting(SettingObject.scanner_runner),
                    'all',
                    '--workspace',
                    get_setting(SettingObject.workspace),
                    '--db_path',
                    db_path,
                    '--extension',
                    get_setting(SettingObject.extension),
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
            raise ValueError('Error in scanning result code: {0}'.format(rc))
        message = 'Scaning done with rc: {0}'.format(rc)
        sublime.status_message(message)
        print(message)
