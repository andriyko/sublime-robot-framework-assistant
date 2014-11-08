#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter (outside of Sublime's python interpreter).

# Python imports
import json
import os

# Plugin imports
try:
    from rfassistant.external import six
except ImportError:
    from ..rfassistant.external import six

if six.PY2:
    from rfassistant import dynamic_data_file_path
else:
    from ..rfassistant import dynamic_data_file_path

if six.PY2:
    class Singleton(type):
        _instances = {}

        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
else:
    class Singleton(type):
        def __init__(cls, *args, **kwargs):
            cls.__instance = None
            super().__init__(*args, **kwargs)

        def __call__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__call__(*args, **kwargs)
                return cls.__instance
            else:
                return cls.__instance


class CachedData(six.with_metaclass(Singleton, object)):
    def __init__(self):
        self._db_path = dynamic_data_file_path
        self.data = {}

    def init(self):
        if self.exists_db():
            with open(self._db_path, 'r+') as f:
                try:
                    self.data = json.load(f)
                except ValueError:
                    self.data = {}
        else:
            with open(self._db_path, 'w'):
                self.data = {}

    def delete_db(self):
        if self.exists_db():
            os.unlink(self._db_path)

    def exists_db(self):
        return os.path.exists(self._db_path)

    def has_file(self, fname):
        return fname in self.data.keys()

    def get_file(self, fname):
        with open(self._db_path, 'r') as f:
            self.data = json.load(f)
            return self.data.get(fname, None)

    def set_file(self, fname, content):
        with open(self._db_path, 'r+') as f:
            try:
                self.data = json.load(f)
            except ValueError:
                self.data = {}
            f.seek(0)
            self.data[fname] = content
            json.dump(self.data, f, indent=4)


class WriteToPanel(six.with_metaclass(Singleton, object)):
    def __init__(self, view):
        self.panel_name = 'rf_panel'
        self.view = view
        self.window = view.window()
        self.output_view = self.window.get_output_panel(self.panel_name)

    def _st2_write_to_panel(self, text):
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.insert(edit, self.output_view.size(), text)
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def _st3_write_to_panel(self, text):
        self.output_view.set_read_only(False)
        self.output_view.run_command('append', {'characters': text})
        self.output_view.set_read_only(True)

    def __call__(self, text):
        if six.PY2:
            self._st2_write_to_panel(text)
        else:
            self._st3_write_to_panel(text)
        self.window.run_command('show_panel', {'panel': 'output.{0}'.format(self.panel_name)})


class StaticDataReader(object):
    @staticmethod
    def get_data(f):
        with open(f) as data_file:
            data = json.load(data_file)
        return data
