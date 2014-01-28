#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
from collections import namedtuple
import os
import tempfile
import webbrowser

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ..rfassistant import PY2

if PY2:
    from mixins import is_robot_var, escape_robot_var, keyword_to_def_name
    from utils import WriteToPanel
    from urllib import quote as url_quote
else:
    from .mixins import is_robot_var, escape_robot_var, keyword_to_def_name
    from .utils import WriteToPanel
    from urllib.parse import quote as url_quote

ALLOW_UNPROMPTED_GO_TO = True
ITEM_TYPE = namedtuple('ITEM_TYPE', 'RESOURCE LIBRARY RFDOCS BUILTIN')('resource', 'library', 'rfdocs', 'builtin')


class RFGlobalVars(object):
    variables = {'${TEMPDIR}': os.path.normpath(tempfile.gettempdir()),
                 '${EXECDIR}': os.path.abspath('.'),
                 '${/}': os.sep,
                 '${:}': os.pathsep,
                 '${SPACE}': ' ',
                 '${EMPTY}': '',
                 '${True}': True,
                 '${False}': False,
                 '${None}': None,
                 '${null}': None,
                 '${OUTPUT_DIR}': '',
                 '${OUTPUT_FILE}': '',
                 '${SUMMARY_FILE}': '',
                 '${REPORT_FILE}': '',
                 '${LOG_FILE}': '',
                 '${DEBUG_FILE}': '',
                 '${PREV_TEST_NAME}': '',
                 '${PREV_TEST_STATUS}': '',
                 '${PREV_TEST_MESSAGE}': '',
                 '${CURDIR}': '.',
                 '${TEST_NAME}': '',
                 '@{TEST_TAGS}': '',
                 '${TEST_STATUS}': '',
                 '${TEST_MESSAGE}': '',
                 '${SUITE_NAME}': '',
                 '${SUITE_SOURCE}': '',
                 '${SUITE_STATUS}': '',
                 '${SUITE_MESSAGE}': ''}


class RFVariable(object):
    def __init__(self, source=None, name=None, value=None):
        self.source = source
        self._name = name
        self.value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not is_robot_var(value):
            raise ValueError('Invalid value given for Robot Framework variable: {0}'.format(value))
        self._name = value

    @property
    def type_(self):
        if not self.source:
            return ITEM_TYPE.BUILTIN
        return self.source.type_

    @property
    def path(self):
        return None if self.type_ == ITEM_TYPE.BUILTIN else self.source.path

    def _select_var_source_in_origin_file(self, view):
        if not view.is_loading():
            s = view.find(r'^\$\{%s\}' % self.name[2:-1], 0, sublime.IGNORECASE)
            if not s:
                return sublime.status_message('Not Found: {0}'.format(self.name))
            view.sel().add(s)
            view.show(s)
            return sublime.status_message('Found: {0}'.format(self.name))
        sublime.status_message('Searching: {0} ...'.format(self.name))
        self._select_var_source_in_origin_file(view)

    # results builders
    def _build_result_string(self, name, type_, path):
        return self.name, '<{0}>'.format(self.type_), self.path

    def build_result_string_for_doc_definitions(self):
        return self._build_result_string(self.name, self.type_, self.path)

    def build_result_string_for_source_definitions(self):
        return self._build_result_string(self.name, self.type_, self.path)

    def build_result_string_for_external_definitions(self):
        return self._build_result_string(self.name, self.type_, self.path)

    # actions
    def show_doc_in_browser(self, view):
        return sublime.status_message('This action is not supported for variables.')

    def show_doc_in_editor(self, view):
        heading = "-"*80
        body = '{name}={value}'.format(name=self.name, value=self.value)
        msg = '\n{heading}\n{body}\n{footer}'.format(heading=heading, body=body, footer=heading)
        WriteToPanel(view)(msg)

    def goto_source(self, view):
        if not self.path:
            return sublime.status_message('This action is not supported for built-in variables.')
        if not os.path.exists(self.path):
            return sublime.error_message('Failed to open file: {0}'.format(self.path))
        vars_file_view = view.window().open_file(self.path)
        sublime.set_timeout(lambda: self._select_var_source_in_origin_file(vars_file_view), 1000)

    def allow_unprompted_go_to(self):
        return ALLOW_UNPROMPTED_GO_TO


class RFKeywordSource(object):
    def __init__(self, library=None, version=None, resource=None, path=None, url=None, noauth_url=None):
        """
        Represents source of the keyword, either Library(local python library),
        Resource(local resource file) or library from rfdocs.org.
        """
        self.library = library
        self.version = version
        self.resource = resource
        self.path = path
        self.url = url
        self.noauth_url = noauth_url

    @property
    def name(self):
        return self.library or self.resource

    @property
    def type_(self):
        if any([self.url, self.noauth_url]):
            return ITEM_TYPE.RFDOCS
        if self.resource:
            return ITEM_TYPE.RESOURCE
        return ITEM_TYPE.LIBRARY

    @property
    def rfdocs_url(self):
        return '{0}/doc'.format(self.noauth_url)

    @property
    def external_url(self):
        return self.url

    def __str__(self):
        if self.type_ == ITEM_TYPE.RFDOCS:
            return '{0} <{1}>'.format(self.name, self.version)
        return '{0} <{1}>'.format(self.name, self.type_)

    # results builders
    def build_result_string_for_doc_definitions(self):
        return self.name, self.type_, self.path or self.rfdocs_url

    def build_result_string_for_external_definitions(self):
        return self.name, self.type_, self.external_url

    def build_result_string_for_source_definitions(self):
        return self.name, self.type_, self.path

    # actions
    def show_doc_in_browser(self, view):
        webbrowser.open(self.external_url)

    def show_doc_in_editor(self, view):
        return sublime.status_message('This action is not supported for local resource: {0}'.format(self.name))

    def goto_source(self, view):
        if self.path and not os.path.exists(self.path):
            return sublime.error_message('Failed to open file: {0}'.format(self.path))
        view.window().open_file(self.path)

    def allow_unprompted_go_to(self):
        return ALLOW_UNPROMPTED_GO_TO


class RFKeyword(object):
    def __init__(self, source, name=None, arguments=None, documentation=None, path=None):
        self.source = source
        self.name = name
        self.arguments = arguments
        self.documentation = documentation
        self._path = path

    def _build_signature(self):
        """
        Transforms keyword name and its arguments into Robot Framework syntax.
        The syntax ${number:text} is a so called 'snippet notation' of Sublime Text.
        This feature allows to jump through arguments with TAB.
        The characters '{' and '}' should be 'escaped' with '{' and '}' accordingly.
        """
        if self.arguments:
            self.arguments = escape_robot_var(self.arguments)
            args = self.arguments.split(',')
            if len(args) == 1:
                return '  ${{1:{0}\n}}'.format(args[0])
            args = '\n'.join(['...  ${{{0}:{1}}}'.format(args.index(arg)+1, arg.strip(),) for arg in args])
            return '\n{0}\n'.format(args)
        return '\n'

    def _select_keyword_source_in_origin_file(self, view):
        if self.type_ == ITEM_TYPE.RESOURCE:
            method = self._find_keyword_in_resource
        else:
            method = self._find_def_in_library
        if not view.is_loading():
            s = method(view)
            if not s:
                return sublime.status_message('Not Found: {0}'.format(self.name))
            view.sel().add(s)
            view.show(s)
            return sublime.status_message('Found: {0}'.format(self.name))
        sublime.status_message('Searching: {0} ...'.format(self.name))
        self._select_keyword_source_in_origin_file(view)

    def _find_def_in_library(self, view):
        def_keyword = keyword_to_def_name(self.name)
        return view.find(r'def\s{0,}%s' % def_keyword, 0, sublime.IGNORECASE)

    def _find_keyword_in_resource(self, view):
        return view.find(r'^%s\s{0,}' % self.name, 0, sublime.IGNORECASE)

    @property
    def signature(self):
        return self._build_signature()

    @property
    def rfdocs_url(self):
        if not self.source.noauth_url:
            return None  # for local library/resource
        quoted_name = url_quote(self.name)
        return '{0}{1}/doc'.format(self.source.noauth_url, quoted_name)

    @property
    def external_url(self):
        if not self.source.url:
            return None  # for local library/resource
        quoted_name = url_quote(self.name)
        return '{0}#{1}'.format(self.source.url, quoted_name)

    @property
    def path(self):
        return self._path if self._path else self.source.path  # will return None for rfdocs keyword

    @property
    def type_(self):
        return self.source.type_

    def get_name_and_signature(self):
        return '{0}{1}'.format(self.name, self.signature)

    def get_source_name(self):
        return self.source.name

    def get_source(self):
        return str(self.source)

    # results builders
    def build_result_string_for_doc_definitions(self):
        return self.name, str(self.source), str(self.path or self.rfdocs_url)

    def build_result_string_for_external_definitions(self):
        return self.name, str(self.source), self.external_url

    def build_result_string_for_source_definitions(self):
        return self.name, str(self.source), self.path

    # actions
    def show_doc_in_browser(self, view):
        webbrowser.open(self.external_url)

    def show_doc_in_editor(self, view):
        if self.type_ == ITEM_TYPE.RFDOCS:
            view.run_command('robot_framework_fetch_keyword_into_view', {'name': self.name, 'url': self.rfdocs_url})
        else:
            heading = "{0:{1}^80}".format(self.name, "-")
            msg = '\n{heading}\n{body}\n{footer}'.format(heading=heading, body=self.documentation, footer='-'*80)
            WriteToPanel(view)(msg)

    def goto_source(self, view):
        path = self.path
        if path and not os.path.exists(path):
            return sublime.error_message('Failed to open file: {0}'.format(path))
        keywords_file_view = view.window().open_file(path)
        sublime.set_timeout(lambda: self._select_keyword_source_in_origin_file(keywords_file_view), 1000)

    def allow_unprompted_go_to(self):
        return ALLOW_UNPROMPTED_GO_TO