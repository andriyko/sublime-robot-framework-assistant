#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import hashlib
import json
import os

try:
    from rfassistant import settings_filename, no_manifest_file, no_libs_dir
    from rfassistant.mixins import url2name
except ImportError:
    from ...rfassistant import settings_filename, no_manifest_file, no_libs_dir
    from ...rfassistant.mixins import url2name


class RobotFrameworkInsertIntoViewCommand(sublime_plugin.TextCommand):
    result = None
    url = None

    def run(self, edit, json_res):
        self.view.insert(edit, 0, json_res)
        self.view.show(0)


class RobotFrameworkValidatePackagesCommand(sublime_plugin.WindowCommand):
    s = None

    def __init__(self, *args, **kwargs):
        super(RobotFrameworkValidatePackagesCommand, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.s = sublime.load_settings(settings_filename)
        self.validate_libs_files()

    def calc_md5(self, f):
        with open(f, 'r') as file_to_check:
            data = file_to_check.read().encode()
            md5_calculated = hashlib.md5(data).hexdigest()
        return md5_calculated

    def validate_libs_files(self):
        validation_failed = False
        result = {}
        libs_manifest = self.s.get('libs_manifest')
        if not os.path.exists(libs_manifest):
            return sublime.error_message(no_manifest_file(libs_manifest))
        libs_dir = self.s.get('libs_dir')
        if not os.path.exists(libs_dir):
            return sublime.error_message(no_libs_dir(libs_dir))
        with open(libs_manifest, 'r') as f:
            content = json.loads(f.read())
        for item in content:
            url = item['url']
            if not url:
                continue
            dir_name = os.path.splitext(url2name(item['url']))[0]
            full_dir_path = os.path.join(libs_dir, dir_name)
            if os.path.exists(full_dir_path) and os.path.isdir(full_dir_path):
                result[dir_name] = []
                for f in item['content']:
                    file_name = f['file']
                    file_md5 = f['md5']
                    file_path = os.path.join(full_dir_path, file_name)
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        md5_is_correct = self.calc_md5(file_path) == file_md5
                        if not md5_is_correct:
                            validation_failed = True
                        result[dir_name].append({file_name: "correct md5" if md5_is_correct else "wrong md5"})
                    else:
                        validation_failed = True
                        result[dir_name].append({file_name: "No such file: {0}".format(file_path)})
            else:
                validation_failed = True
                result[dir_name] = 'No such directory: {0}'.format(full_dir_path)
        result['validation_result'] = "Validation failed" if validation_failed else "Validation passed"
        json_res = json.dumps(result, indent=4)
        self.window.new_file()
        self.window.run_command("robot_framework_insert_into_view", {"json_res": json_res})
        self.window.focus_group(0)