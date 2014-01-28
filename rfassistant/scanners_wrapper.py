#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter (outside of Sublime's python interpreter).

# Python imports
import os

# Plugin imports
from mixins import is_python_file


def get_modules(dirname):
    modules = set()
    for f in os.listdir(dirname):
        path = os.path.join(dirname, f)
        basename = os.path.splitext(os.path.basename(path))[0]
        if all([os.path.isfile(path), is_python_file(path), not basename.startswith('_')]):
            modules.add(basename)
    return modules


class ScannersWrapper(object):
    def __init__(self, modules):
        for module in modules:
            if not self._is_module_scanner(module):
                continue
            attrlist = self._get_attrs(module)
            for attr in [a for a in attrlist if '__' not in a]:
                attr_obj = getattr(module, attr)
                if not self._is_class_scanner(attr_obj):
                    continue
                if hasattr(self, attr):
                    raise AttributeError('Already set: {0}'.format(attr))
                setattr(self, attr, attr_obj)

    def _is_module_scanner(self, obj):
        return getattr(obj, 'is_scanner', False)

    def _is_class_scanner(self, obj):
        return any(
            [getattr(obj, attr, False) for attr in ('is_pylib_scanner', 'is_resource_scanner', 'is_testcase_scanner')]
        )

    def _get_attrs(self, obj):
        try:
            attrs_list = obj.__all__
        except AttributeError:
            attrs_list = dir(obj)
        return attrs_list
