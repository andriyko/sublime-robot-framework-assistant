import sublime_plugin
import sublime
import subprocess
import os
import sys
import logging


class ScanIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print('HERE')
        plugin_settings = sublime.load_settings('RobotFrameworkDataEditor.sublime-settings')
        print(plugin_settings)
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
