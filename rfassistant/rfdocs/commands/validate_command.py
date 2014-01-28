#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
import hashlib
import json
import os

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ....rfassistant import PY2

if PY2:
    from rfassistant.settings import settings
    from rfassistant import no_manifest_file, no_libs_dir
    from rfassistant.mixins import url2name
else:
    from ....rfassistant.settings import settings
    from ....rfassistant import no_manifest_file, no_libs_dir
    from ....rfassistant.mixins import url2name


class RobotFrameworkInsertIntoViewCommand(sublime_plugin.TextCommand):
    result = None
    url = None

    def run(self, edit, json_res):
        self.view.insert(edit, 0, json_res)
        self.view.show(0)


class RobotFrameworkValidatePackagesCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(RobotFrameworkValidatePackagesCommand, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.validate_libs_files()

    def calc_md5(self, f):
        with open(f, 'r') as file_to_check:
            data = file_to_check.read().encode()
            md5_calculated = hashlib.md5(data).hexdigest()
        return md5_calculated

    def validate_libs_files(self):
        validation_failed = False
        result = {}
        rfdocs_manifest = settings.rfdocs_manifest
        if not os.path.exists(rfdocs_manifest):
            return sublime.error_message(no_manifest_file(rfdocs_manifest))
        rfdocs_dir = settings.rfdocs_dir
        if not os.path.exists(rfdocs_dir):
            return sublime.error_message(no_libs_dir(rfdocs_dir))
        with open(rfdocs_manifest, 'r') as f:
            content = json.loads(f.read())
        for item in content:
            url = item['url']
            if not url:
                continue
            dir_name = os.path.splitext(url2name(item['url']))[0]
            full_dir_path = os.path.join(rfdocs_dir, dir_name)
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
        self.window.run_command("rfa_insert_into_view", {"json_res": json_res})
        self.window.focus_group(0)