#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .external import six

plugin_name = 'Robot Framework Assistant'
settings_filename = '{0}.sublime-settings'.format(plugin_name)
no_manifest_file = lambda x: 'Failed to open manifest file. ' \
                             'Please download manifest first. No such file: {0}'.format(x)
no_libs_dir = lambda x: 'Failed to open libraries directory. ' \
                        'Please download packages first. No such file or directory: {0}'.format(x)


def mkdir_safe(p, safeguard):
    if not os.path.exists(p) and p.startswith(safeguard):
        os.makedirs(p)


libs_update_url_default = "http://rfdocs.org/dataset/download?"
package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
robot_data_dir_path = os.path.join(package_dir, 'robot_data')
mkdir_safe(robot_data_dir_path, package_dir)
libs_manifest_path = os.path.join(robot_data_dir_path, 'libs_manifest.json')
libs_dir_path = os.path.join(robot_data_dir_path, 'libs')
mkdir_safe(libs_dir_path, package_dir)
tmp_dir_path = os.path.join(robot_data_dir_path, 'tmp')
mkdir_safe(tmp_dir_path, package_dir)

if six.PY2:
    robot_tm_language_path = os.path.join(package_dir, "robot.tmLanguage")
else:
    robot_tm_language_path = os.path.join(os.path.basename(os.path.dirname(package_dir)),
                                      os.path.basename(package_dir),
                                      "robot.tmLanguage")