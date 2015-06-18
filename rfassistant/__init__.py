#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from external import six
except ImportError:
    from .external import six

PY2 = six.PY2


def mkdir_safe(p, safeguard):
    if not os.path.exists(p) and p.startswith(safeguard):
        os.makedirs(p)


plugin_name = 'Robot Framework Assistant'
__version__ = VERSION = plugin_version = '1.2.2'
plugin_home = 'https://github.com/andriyko/sublime-robot-framework-assistant'
py_version = '2' if PY2 else '3'
user_agent = '{0}/{1}/{2}'.format(plugin_name, plugin_version, py_version)

syntax_file = 'robot.tmLanguage'
settings_filename = '{0}.sublime-settings'.format(plugin_name)
no_manifest_file = lambda x: 'Failed to open manifest file. ' \
                             'Please download manifest first. No such file: {0}'.format(x)
no_libs_dir = lambda x: 'Failed to open libraries directory. ' \
                        'Please download packages first. No such file or directory: {0}'.format(x)
no_python_path = lambda x: 'Could not add path to system.path. ' \
                           'No such file or directory: {0}'.format(x)

no_python_interpreter = lambda x: \
    'Could not use Python interpreter. No such file or directory: {0}. ' \
    'Please specify Python interpreter with Robot Framework installed.'.format(x)

package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

robot_data_dir_path = os.path.join(package_dir, 'robot_data')
mkdir_safe(robot_data_dir_path, package_dir)

current_tmp_dir_path = os.path.join(robot_data_dir_path, 'current')
mkdir_safe(current_tmp_dir_path, robot_data_dir_path)

dynamic_data_file_path = os.path.join(current_tmp_dir_path, 'current_data.json')

rfdocs_update_url = "http://rfdocs.org/api/v1/"

rfdocs_base_dir_path = os.path.join(robot_data_dir_path, 'rfdocs')
mkdir_safe(rfdocs_base_dir_path, package_dir)

rfdocs_manifest_path = os.path.join(rfdocs_base_dir_path, 'manifest.json')

rfdocs_dir_path = os.path.join(rfdocs_base_dir_path, 'libraries')
mkdir_safe(rfdocs_dir_path, package_dir)

rfdocs_tmp_dir_path = os.path.join(rfdocs_base_dir_path, 'tmp')
mkdir_safe(rfdocs_tmp_dir_path, package_dir)

scanner_config_path = os.path.join(package_dir, 'scanners.example.json')

user_scanners_dir_path = os.path.join(package_dir, 'user_scanners')

python_libs_dir_path = os.path.join(robot_data_dir_path, 'libraries')
mkdir_safe(python_libs_dir_path, package_dir)

resources_dir_path = os.path.join(robot_data_dir_path, 'resources')
mkdir_safe(resources_dir_path, package_dir)

variables_dir_path = os.path.join(robot_data_dir_path, 'variables')
mkdir_safe(variables_dir_path, package_dir)

rflint_setting_filename = '{0} Rflint.sublime-settings'.format(plugin_name)

if PY2:
    robot_tm_language_path = os.path.join(package_dir, syntax_file)
else:
    robot_tm_language_path = "Packages/{0}/{1}".format(plugin_name, syntax_file)
