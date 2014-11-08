#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter (outside of Sublime's python interpreter).


from abc import ABCMeta, abstractmethod
import inspect
import os

# robot imports
from robot import parsing

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ..rfassistant import PY2

if PY2:
    from mixins import clean_robot_var
else:
    from .mixins import clean_robot_var


class ResourceAndTestCaseFileParserAbstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_keywords(self):
        raise NotImplementedError

    @abstractmethod
    def get_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_variables(self):
        raise NotImplementedError

    @abstractmethod
    def get_path(self):
        raise NotImplementedError

    @abstractmethod
    def get_data(self):
        raise NotImplementedError


class ResourceAndTestCaseFileParserBase(ResourceAndTestCaseFileParserAbstract):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            raise IOError(self.path)
        self.parsed = self._parse()

    def _parse(self):
        raise NotImplementedError('Must be implemented in subclass!')

    def get_path(self):
        return self.path

    def get_name(self):
        return self.parsed.name

    def get_keywords(self):
        return [
            {
                'name': kw.name,
                'arguments': ', '.join([clean_robot_var(val) for val in kw.args.value]),
                'documentation': kw.doc.value
            }
            for kw in self.parsed.keywords
        ]

    def get_variables(self):
        return [
            {
                'name': var.name,
                'value': ', '.join(var.value)
            }
            for var in self.parsed.variable_table.variables
        ]

    def get_data(self):
        return {
            'keywords': self.get_keywords(),
            'variables': self.get_variables(),
            'path': self.get_path(),
            'resource': self.get_name()
        }


class ResourceFileParserBase(ResourceAndTestCaseFileParserBase):
    def _parse(self):
        return parsing.ResourceFile(source=self.path).populate()


class TestCaseFileParserBase(ResourceAndTestCaseFileParserBase):
    def _parse(self):
        return parsing.TestCaseFile(source=self.path).populate()


class PythonLibParserAbstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_library_keywords(self):
        raise NotImplementedError

    @abstractmethod
    def get_library_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_library_version(self):
        raise NotImplementedError

    @abstractmethod
    def get_library_path(self):
        raise NotImplementedError


class PythonLibParserBase(PythonLibParserAbstract):
    def __init__(self, library):
        self.library = library

    def _def_name_to_keyword(self, name):
        name = name.replace('_', ' ').strip()
        return name.title() if name.islower() else name

    def _keyword_to_def_name(self, name):
        name = name.replace(' ', '_').strip()
        return name.lower()

    def _library_is_class(self):
        return inspect.isclass(self.library)

    def _library_is_module(self):
        return inspect.ismodule(self.library)

    def _get_inspection_predicate(self):
        return inspect.ismethod if self._library_is_class() else inspect.isfunction

    def _get_class(self, meth):
        for cls in inspect.getmro(meth.im_class):
            if meth.__name__ in cls.__dict__:
                return cls
        return None

    def _get_class_keywords(self):
        keywords = []
        library_path = self.get_library_path()
        # 'get_keyword_names' - isn't reliable
        # if hasattr(self.library, 'get_keyword_names'):
        #     class_members = [
        #         (func_name, getattr(self.library, func_name)) for func_name in self.library().get_keyword_names()
        #     ]
        # else:
        #     class_members = inspect.getmembers(self.library, predicate=inspect.ismethod)
        class_members = inspect.getmembers(self.library, predicate=inspect.ismethod)
        for member in class_members:
            func_name, func_obj = member[0], member[1]
            if func_name.startswith('_'):
                continue
            # get function's signature
            # Read more here: http://docs.python.org/2/library/inspect.html#inspect.getargspec
            func_signature = inspect.getargspec(func_obj)
            # handle _defaults correctly
            if func_signature.defaults:
                defaults = dict(zip(reversed(func_signature.args), reversed(func_signature.defaults)))
                # exclude args that are already in _defaults
                _args = [arg for arg in func_signature.args if arg not in defaults]
                # exclude `self`
                args = _args[1:] if _args[0] == 'self' else _args
                for k, v in defaults.iteritems():
                    args.append('{0}={1}'.format(k, v))
            else:
                # exclude `self`
                args = func_signature.args[1:] if func_signature.args[0] == 'self' else func_signature.args
            if func_signature.varargs:
                args.append('*%s' % func_signature.varargs)
            name = self._def_name_to_keyword(func_name)

            # now try to find real source of the method
            klass = self._get_class(func_obj)
            kw = {'name': name, 'arguments': ', '.join(args), 'documentation': func_obj.__doc__}
            if klass:
                klass_source = inspect.getsourcefile(klass)
                if klass_source and klass_source != library_path:
                    kw['path'] = klass_source
            keywords.append(kw)

        return keywords

    def _get_module_keywords(self):
        keywords = []
        library_path = self.get_library_path()
        the_all_attribute = getattr(self.library, '__all__', [])
        if the_all_attribute:
            module_members = [(func_name, getattr(self.library, func_name)) for func_name in the_all_attribute]
        else:
            module_members = inspect.getmembers(self.library, predicate=inspect.isfunction)
        for member in module_members:
            func_name, func_obj = member[0], member[1]
            if func_name.startswith('_'):
                continue
            # get function's signature
            # Read more here: http://docs.python.org/2/library/inspect.html#inspect.getargspec
            func_signature = inspect.getargspec(func_obj)
            # handle _defaults correctly
            if func_signature.defaults:
                defaults = dict(zip(reversed(func_signature.args), reversed(func_signature.defaults)))
                # exclude args that are already in _defaults
                args = [arg for arg in func_signature.args if arg not in defaults]
                for k, v in defaults.iteritems():
                    args.append('{0}={1}'.format(k, v))
            else:
                args = func_signature.args
                # handle varargs
            if func_signature.varargs:
                args.append('*%s' % func_signature.varargs)
            name = self._def_name_to_keyword(func_name)

            # now try to find real source of the function
            func_source = inspect.getsourcefile(func_obj)
            kw = {'name': name, 'arguments': ', '.join(args), 'documentation': func_obj.__doc__}
            if func_source and func_source != library_path:
                kw['path'] = func_source
            keywords.append(kw)

        return keywords

    def get_library_name(self):
        if self._library_is_class():
            return self.library.__name__
        elif self._library_is_module():
            return self.library.__name__.split('.')[-1]
        return str(self.library)

    def get_library_version(self):
        _get_version = lambda obj: getattr(obj, '__version__', None) or getattr(obj, 'get_version', lambda: None)()
        if self._library_is_class():
            return _get_version(inspect.getmodule(self.library))
        elif self._library_is_module():
            return _get_version(self.library)

    def get_library_path(self):
        return inspect.getsourcefile(self.library)

    def get_library_keywords(self):
        if self._library_is_class():
            return self._get_class_keywords()
        elif self._library_is_module():
            return self._get_module_keywords()
        else:
            raise RuntimeError('Failed to get keywords')
