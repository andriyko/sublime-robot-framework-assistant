import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting
from ..setting.setting import SettingObject


class ScanOpenTabCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Command to scan open tab RF file and create db table

        Purpose of the command is scan and create the db table
        from the currently open tab.
        """
        log_file = get_setting(SettingObject.log_file)
        python_binary = get_setting(SettingObject.python_binary)
        table_dir = get_setting(SettingObject.table_dir)
        makedirs(path.dirname(log_file), exist_ok=True)
        open_tab = self.view.file_name()
        if self.file_in_workspace(open_tab):
            file_ = open(log_file, 'w')
            sublime.set_timeout_async(self.run_single_scan(
                    python_binary,
                    table_dir,
                    file_
                ), 0)
            file_.close()
            file_.close()
        else:
            message = 'Not able to scan file: {0}'.format(open_tab)
            sublime.status_message(message)

    def run_single_scan(self, python_binary, db_path, log_file):
        open_tab = self.view.file_name()
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
                [
                    python_binary,
                    get_setting(SettingObject.scanner_runner),
                    'single',
                    '--path_to_file',
                    open_tab,
                    '--db_path',
                    db_path,
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

    def file_in_workspace(self, open_tab):
        workspace = get_setting(SettingObject.workspace)
        workspace = path.normcase(workspace)
        open_tab = path.normcase(open_tab)
        extension = get_setting(SettingObject.extension)
        if open_tab.endswith(extension):
            return open_tab.startswith(workspace)
        else:
            return False
