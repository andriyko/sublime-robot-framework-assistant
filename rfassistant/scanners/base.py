#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter
# (outside of Sublime's python interpreter).
from __future__ import print_function

from abc import ABCMeta, abstractmethod
import os
import sys

from rfassistant.parsers.standard import (PythonLibParserStandard, ResourceFileParserStandard,
                                          TestCaseFileParserStandard)
from rfassistant.mixins import is_robot_language_file

# robot imports
from robot import errors as robot_errors


def get_resource_files(dir_name):
    for root, dirs, files in os.walk(dir_name):
        for f in files:
            yield os.path.join(root, f)


class ScannerAbstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def scan(cls):
        raise NotImplementedError


class ResourceFilesScannerBase(ScannerAbstract):
    is_resource_scanner = True

    @classmethod
    def produce_result(cls, parser):
        return parser.get_data()

    @classmethod
    def scan(cls, *args, **kwargs):
        path = kwargs.get('path')
        extensions = kwargs.get('associated_file_extensions',
                                ['.txt', '.robot'])
        if os.path.exists(path):
            if os.path.isdir(path):
                for f in get_resource_files(path):
                    if is_robot_language_file(f, extensions):
                        try:
                            parser = ResourceFileParserStandard(f)
                            yield parser.get_data()
                        except robot_errors.DataError as err:
                            print('Failed to parse file: {0}. '
                                  'Error was: {1}'.format(f, err),
                                  file=sys.stderr)
                            yield None
            if os.path.isfile(path):
                try:
                    parser = ResourceFileParserStandard(path)
                    yield parser.get_data()
                except robot_errors.DataError as err:
                    print('Failed to parse file: {0}. '
                          'Error was: {1}'.format(path, err), file=sys.stderr)
                    yield None
        else:
            raise IOError('Failed to scan resources. '
                          'No such file or directory: {0}'.format(path))


class TestCaseFilesScannerBase(ScannerAbstract):
    is_testcase_scanner = True

    @classmethod
    def produce_result(cls, parser):
        return parser.get_data()

    @classmethod
    def scan(cls, *args, **kwargs):
        path = kwargs.get('path')
        if not os.path.isfile(path):
            raise IOError('Expected file instead of: {0}'.format(path))
        parser = TestCaseFileParserStandard(path)
        yield parser.get_data()


class PythonLibsScannerBase(ScannerAbstract):
    is_pylib_scanner = True
    __asterisk = '*'

    @classmethod
    def produce_result(cls, parser):
        return {
            'library': parser.get_library_name(),
            'version': parser.get_library_version(),
            'path': parser.get_library_path(),
            'keywords': parser.get_library_keywords()
        }

    @classmethod
    def handle_no_package_or_libraries(cls, lib):
        """
        Handle scanner configuration with empty
        'package' option or emtpy 'libraries' option.

        If 'libraries' option is not defined, fromlist is '*'.

        If 'package' option is not defined, each entry from 'libraries' options
        is treated as a separate package(module).
        """
        try:
            module = __import__(lib, fromlist=cls.__asterisk)
        except ImportError:
            return
        # is library implemented as python class?
        library_class = getattr(module, lib, None)
        # now library is either class or module
        library = library_class if library_class else module
        parser = PythonLibParserStandard(library)
        yield cls.produce_result(parser)

    @classmethod
    def scan(cls, *args, **kwargs):
        package = kwargs['package']
        libraries = [str(arg) for arg in args]

        if not any([package, libraries]):
            raise RuntimeError('Invalid scanner configuration. '
                               'Need at least one option, either '
                               '\'package\' or \'libraries\' to be defined.')

        if not package and libraries:
            # cases like
            # >>> import SSHLibrary, Selenium2Library, SeleniumLibrary
            for library in libraries:
                yield cls.handle_no_package_or_libraries(library)

        elif not libraries and package:
            # cases like
            # >>> import SSHLibrary
            yield cls.handle_no_package_or_libraries(package)

        elif package and libraries:
            # cases like
            # >>> from robot.libraries import BuiltIn, String, Collections
            try:
                module = __import__(package, fromlist=libraries)
            except ImportError:
                return
            for library in libraries:
                library_module = getattr(module, library)
                # is library implemented as python class?
                library_class = getattr(library_module, library, None)
                # now library is either class or module
                library = library_class if library_class else library_module
                parser = PythonLibParserStandard(library)
                yield cls.produce_result(parser)
