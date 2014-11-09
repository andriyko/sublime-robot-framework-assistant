#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should to be used with system python interpreter
# (outside of Sublime's python interpreter).

# Python imports
import json
import os
import shutil
import sys
import types

# Plugin imports
from rfassistant.utils import CachedData
from scanners import __scanners__
from rfassistant.user_scanners import __user_scanners__


def _prepare_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)


def _get_scanner_conf(scanner_conf):
    with open(scanner_conf, 'r') as f:
        return json.load(f)


def run_pylib_scanner(scanner_conf_path, python_libs_dir):
    _prepare_directory(python_libs_dir)

    scanner_conf = _get_scanner_conf(scanner_conf_path)

    paths_to_add = scanner_conf['paths']
    if paths_to_add:
        sys.path.extend(paths_to_add)

    scanners_data = scanner_conf['pylib_scanners']
    for scanner in scanners_data:
        if not scanner['is_active']:
            continue
        parser_class = scanner['parser']
        module_name, class_name = parser_class.rsplit('.', 1)
        module_path = os.path.join(python_libs_dir, *module_name.split('.'))
        if not os.path.exists(module_path):
            os.makedirs(module_path)
        if hasattr(__user_scanners__, class_name):
            scanner_class = getattr(__user_scanners__, class_name)
        else:
            scanner_class = getattr(__scanners__, class_name)
        libs = scanner_class.scan(*scanner['libraries'],
                                  package=scanner['package'])
        for lib in libs:
            if isinstance(lib, types.GeneratorType):
                for nested_lib in lib:
                    with open('{0}.json'.format(os.path.join(
                            module_path, nested_lib['library'])), 'w') as f:
                        json.dump(nested_lib, f, indent=4)
            else:
                with open('{0}.json'.format(os.path.join(
                        module_path, lib['library'])), 'w') as f:
                    json.dump(lib, f, indent=4)


def run_resource_scanner(scanner_conf_path, resources_dir, settings):
    _prepare_directory(resources_dir)

    scanner_conf = _get_scanner_conf(scanner_conf_path)

    paths_to_add = scanner_conf['paths']
    if paths_to_add:
        sys.path.extend(paths_to_add)

    scanners_data = scanner_conf['resource_scanners']
    for scanner in scanners_data:
        if not scanner['is_active']:
            continue
        parser_class = scanner['parser']
        module_name, class_name = parser_class.rsplit(".", 1)
        module_path = os.path.join(resources_dir, *module_name.split('.'))
        if not os.path.exists(module_path):
            os.makedirs(module_path)
        if hasattr(__user_scanners__, class_name):
            scanner_class = getattr(__user_scanners__, class_name)
        else:
            scanner_class = getattr(__scanners__, class_name)
        resources = scanner_class.scan(
            path=scanner['path'],
            associated_file_extensions=settings['associated_file_extensions']
        )
        for resource in resources:
            if not resource:
                continue
            target = '{0}.json'.format(os.path.join(module_path,
                                                    resource['resource']))
            _dir, _fname = os.path.split(target)
            parts = os.path.split(resource['path'])[0].split(os.sep)
            new_parts = []
            while os.path.exists(target) and parts:
                new_parts.append(parts.pop())
                target = os.path.join(
                    _dir, '{0}.{1}'.format('.'.join(new_parts), _fname)
                )
            with open(target, 'w') as f:
                json.dump(resource, f, indent=4)


def run_testcase_scanner(scanner_conf_path, file_to_scan):
    scanner_conf = _get_scanner_conf(scanner_conf_path)
    testcase_scanner = scanner_conf['testcase_scanner']
    if not testcase_scanner['is_active']:
        return
    parser_class = testcase_scanner['parser']
    module_name, class_name = parser_class.rsplit(".", 1)
    if hasattr(__user_scanners__, class_name):
        scanner_class = getattr(__user_scanners__, class_name)
    else:
        scanner_class = getattr(__scanners__, class_name)
    result = list(scanner_class.scan(path=file_to_scan))[0]
    cache = CachedData()
    cache.init()
    cache.set_file(file_to_scan, result)


if __name__ == '__main__':
    scanner_type = sys.argv[1]
    if scanner_type == 'pylib':
        run_pylib_scanner(sys.argv[2], sys.argv[3])
    elif scanner_type == 'resource':
        run_resource_scanner(sys.argv[2], sys.argv[3], json.loads(sys.argv[4]))
    elif scanner_type == 'testcase':
        run_testcase_scanner(sys.argv[2], sys.argv[3])