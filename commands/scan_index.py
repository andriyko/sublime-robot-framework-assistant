import sublime_plugin
import sublime
import subprocess
from platform import system
from os import path, makedirs
from ..setting.setting import get_setting


class ScanIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        scanner_dir = get_setting('scanner_dir')
        robot_framework_workspace = get_setting('robot_framework_workspace')
        extension = get_setting('robot_frameowrk_extension')
        python_binary = get_setting('path_to_python')
        log_file = get_setting('log_file')
        makedirs(path.dirname(log_file), exist_ok=True)
        file_ = open(log_file, 'w')
        sublime.set_timeout_async(self.run_scan(
                python_binary,
                robot_framework_workspace,
                extension,
                scanner_dir,
                file_
            ), 0)
        index_dir = get_setting('index_dir')
        sublime.set_timeout_async(self.run_index(
                python_binary,
                scanner_dir,
                index_dir,
                file_
            ), 0)
        file_.close()

    def run_scan(
            self,
            python_binary,
            workspace,
            extension,
            db_path,
            log_file):
        run_scanner = get_setting('scanner_runner')
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
            [python_binary,
             run_scanner,
             'all',
             '--workspace',
             workspace,
             '--db_path',
             db_path,
             '--extension',
             extension],
            stderr=subprocess.STDOUT,
            stdout=log_file,
            startupinfo=startupinfo
        )
        rc = p.wait()
        print('Scaning done with rc: ', rc)

    def run_index(
            self,
            python_binary,
            db_path,
            index_path,
            log_file):
        run_index = get_setting('index_runner')
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
            [python_binary,
             run_index,
             'all',
             '--db_path',
             db_path,
             '--index_path',
             index_path],
            stderr=subprocess.STDOUT,
            stdout=log_file,
            startupinfo=startupinfo
        )
        rc = p.wait()
        print('Indexing done with rc: ', rc)
