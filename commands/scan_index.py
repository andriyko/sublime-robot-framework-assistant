import sublime_plugin
import sublime
import subprocess
import os
from ..setting.setting import get_setting


class ScanIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print('HERE')
        scanner_dir = get_setting('scanner_dir')
        print(scanner_dir)
        robot_framework_workspace = get_setting('robot_framework_workspace')
        print(robot_framework_workspace)
        sublime.set_timeout_async(self.run_scan, 0)

    def run_scan(self):
        c_dir = os.path.dirname(os.path.realpath(__file__))
        run_scanner = os.path.realpath(
            os.path.join(
                c_dir,
                '..',
                'dataparser',
                'run_scanner.py')
        )
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        log_file = open('D:\\popen.log', 'w')
        p = subprocess.Popen(
            ['C:\\Python27\\python.exe',
             run_scanner, 'all',
             '--workspace',
             'D:\\workspace\\robotframework-from-sublime\\test\\resource\\test_data\\suite_tree',
             '--db_path',
             'D:\\db_path',
             '--extension',
             'robot'],
            stderr=subprocess.STDOUT,
            stdout=log_file,
            startupinfo=startupinfo
        )
        rc = p.wait()
        print('rc: ', rc)
