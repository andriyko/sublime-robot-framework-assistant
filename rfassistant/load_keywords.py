#!/usr/bin/env python
import sublime
import sublime_plugin

import json
import os
import threading
import re
import webbrowser
import weakref

try:
    from rfassistant.external import six
except ImportError:
    from ..rfassistant.external import six

if six.PY2:
    from urllib import quote as url_quote
    from rfassistant import settings_filename, no_libs_dir
    from mixins import is_json_file, is_robot_or_txt_file, is_robot_format
else:
    from urllib.parse import quote as url_quote
    from ..rfassistant import settings_filename, no_libs_dir
    from .mixins import is_json_file, is_robot_or_txt_file, is_robot_format

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

    class Cached(type):
        def __init__(cls, *args, **kwargs):
            super().__init__(*args, **kwargs)
            cls.__cache = weakref.WeakValueDictionary()

        def __call__(cls, *args):
            if args in cls.__cache:
                return cls.__cache[args]
            else:
                obj = super().__call__(*args)
                cls.__cache[args] = obj
                return obj


def select_keyword_and_do_action(view, results, action):
    # action either 'show_definition' or 'insert_doc'
    def on_done(index):
        if index == -1:
            return
        getattr(results[index], action)(view)

    if len(results) == 1 and results[0].allow_unprompted_go_to():
        getattr(results[0], action)(view)
        return
    attr = 'url' if action == 'show_definition' else 'noauth_url'
    result_strings = [
        [kw.name, '{0:10} {1}'.format('Library:', kw.library),
         '{0:9} {1}'.format('Version:', kw.version), getattr(kw, attr), ] for kw in results
    ]
    view.window().show_quick_panel(result_strings, on_done)


def get_keyword_at_pos(line, col):
    length = len(line)
    if length == 0:
        return None
    # between spaces
    if all([col >= length or line[col] == ' ' or line[col] == "\t",
            col == 0 or line[col-1] == ' ' or line[col-1] == "\t"]):
        return None
    # first look back until we find 2 spaces in a row, or reach the beginning
    i = col - 1
    while i >= 0:
        if line[i] == "\t" or all([line[i - 1] == ' ' or line[i - 1] == '|',
                                   line[i] == ' ']):
            break
        i -= 1
    begin = i + 1
    # now look forward or until the end
    i = col  # previous included line[col]
    while i < length:
        if line[i] == "\t" or (line[i] == " " and len(line) > i and (line[i + 1] == " " or line[i + 1] == '|')):
            break
        i += 1
    end = i
    return line[begin:end]


class RFKeyword(object):
    _name = ""
    _arguments = ""
    _signature = ""
    _library = ""
    _version = ""

    def __init__(self, name, arguments, library, version):
        self._name = name
        self._library = library
        self._arguments = arguments
        self._version = version
        self._signature = self.get_signature()

    def get_signature(self):
        """
        Transforms keyword name and its arguments into Robot Framework syntax.

        The syntax ${number:text} is a so called 'snippet notation' of Sublime Text.
        This feature allows to jump through arguments with TAB.
        The characters '{' and '}' should be 'escaped' with '{' and '}' accordingly.
        """
        if self._arguments:
            args = self._arguments.split(',')
            if len(args) == 1:
                return '  ${{1:{0}\n}}'.format(args[0])
            args = '\n'.join(['...  ${{{0}:{1}}}'.format(args.index(arg)+1, arg.strip(),) for arg in args])
            return '\n{0}\n'.format(args)
        return '\n'

    def get_name_and_signature(self):
        return '{0}{1}'.format(self._name, self._signature)

    def get_version_and_library(self):
        return '{0}.{1}'.format(self._version, self._library)

    def get_library_and_version(self):
        return '{0}.{1}'.format(self._library, self._version)

    def get_library(self):
        return self._library

    @property
    def name(self):
        return self._name

    @property
    def signature(self):
        return self._signature

    @property
    def library(self):
        return self._library

    @property
    def version(self):
        return self._version


class RFWebKeyword(object):
    def __init__(self, name, library, version, url, noauth_url):
        self.name = name
        self.library = library
        self.version = version
        self.url = url
        self.noauth_url = noauth_url

    def show_definition(self, view):
        webbrowser.open(self.url)

    def insert_doc(self, view):
        view.run_command("robot_framework_fetch_keyword_into_view", {"url": self.noauth_url})

    def allow_unprompted_go_to(self):
        return False


class GoToWebKeywordThread(threading.Thread):
    def __init__(self, view, view_file, results, method, action):
        self.view = view
        self.view_file = view_file
        self.results = results
        self.method = method
        self.action = action
        threading.Thread.__init__(self)

    def run(self):
        sublime.set_timeout(lambda: self.method(self.view, self.results, self.action), 0)


class RFKeywordAggregateAutoCompleteListAndDefinitions(six.with_metaclass(Singleton, object)):

    def __init__(self):
        self._autocomplete = []
        self._autocomplete_method = 'get_library'
        self._web_definitions = {}

    def set_autocomplete_method(self, method):
        self._autocomplete_method = method

    def clear_autocomplete(self):
        self._autocomplete = []

    def clear_web_definitions(self):
        self._web_definitions = {}

    def clear_data(self):
        self.clear_autocomplete()
        self.clear_web_definitions()

    def has_autocomplete(self):
        return self._autocomplete != []

    def has_web_definitions(self):
        return self._web_definitions != {}

    def has_data(self):
        return all([self.has_autocomplete(), self.has_web_definitions(), ])

    def add_kw_for_autocomplete(self, name, arguments, library, version):
        self._autocomplete.append(RFKeyword(name, arguments, library, version))

    def add_kw_for_web_definitions(self, name, library, version, url, noauth_url):
        quoted_name = url_quote(name)
        self._web_definitions.setdefault(name, set()).add(RFWebKeyword(name,  library, version,
                                                                       '{0}#{1}'.format(url, quoted_name),
                                                                       '{0}{1}/doc'.format(noauth_url, quoted_name),))

    def get_autocomplete_list(self, word):
        return [(kw.name + '\t' + getattr(kw, self._autocomplete_method)(),
                 kw.get_name_and_signature()) for kw in self._autocomplete if word.lower() in kw.name.lower()]

    def get_web_definitions_list(self, word):
        definitions_list = []
        if word in self._web_definitions:
            definitions_list.extend(self._web_definitions[word])
        return definitions_list


class RFKeywordCollectorThread(threading.Thread):

    def __init__(self, collector, keywords_lookup_dir, timeout_seconds):
        self.view = sublime.active_window().active_view()
        self.collector = collector
        self.timeout = timeout_seconds
        self.keywords_lookup_dir = keywords_lookup_dir
        self.status_name = 'rf_collector'
        threading.Thread.__init__(self)

    def save_keyword(self, file_name):
        sublime.set_timeout(
            lambda: self.view.set_status(self.status_name,
                                         'Loading data from: {0}'.format(os.path.basename(file_name))), 100
        )
        with open(file_name) as data_file:
            data = json.load(data_file)
        library = data['library']
        version = data['version']
        url = data['url']
        noauth_url = data['noauth_url']
        for kw in data['keywords']:
            name = kw['name']
            self.collector.keywords_owner.add_kw_for_web_definitions(name, library, version, url, noauth_url)
            self.collector.keywords_owner.add_kw_for_autocomplete(name, kw['arguments'], library, version)
        sublime.set_timeout(lambda: self.view.erase_status(self.status_name), 100)

    def get_json_files(self, dir_name, *args):
        files_list = []
        d = os.path.join(self.keywords_lookup_dir, dir_name)
        if not os.path.isdir(d):
            return files_list
        for f in os.listdir(d):
            dirfile = os.path.join(d, f)
            if os.path.isfile(dirfile):
                if is_json_file(dirfile):
                    files_list.append(dirfile)
            elif os.path.isdir(dirfile):
                files_list += self.get_json_files(dirfile, *args)
        return files_list

    def run(self):
        for folder in os.listdir(self.keywords_lookup_dir):
            json_files = self.get_json_files(folder)
            for file_name in json_files:
                self.save_keyword(file_name)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class RFKeywordCollector(sublime_plugin.EventListener):

    _collector_thread = None

    def __init__(self, *args, **kwargs):
        super(RFKeywordCollector, self).__init__(*args, **kwargs)
        if six.PY2:
            setattr(self, 'on_load', self._on_load)
        else:
            setattr(self, 'on_load_async', self._on_load)
            setattr(self, 'on_activated', self._on_activated)
        self.keywords_owner = RFKeywordAggregateAutoCompleteListAndDefinitions()

    def _collect_keywords(self):
        self.s = sublime.load_settings(settings_filename)
        libs_dir = str(self.s.get('libs_dir'))
        if not os.path.exists(libs_dir):
            return
        self.keywords_owner.set_autocomplete_method(self.get_method_for_autocomplete())
        self.keywords_owner.clear_data()
        if self._collector_thread is not None:
            self._collector_thread.stop()
        self._collector_thread = RFKeywordCollectorThread(self, libs_dir, 30)
        self._collector_thread.start()

    def _on_load(self, view):
        if not is_robot_format(view):
            return
        if self.keywords_owner.has_data():
            return
        self._collect_keywords()

    def _on_activated(self, view):
        if not is_robot_format(view):
            return
        if self.keywords_owner.has_data():
            return
        self._collect_keywords()

    def get_method_for_autocomplete(self):
        method = 'get_library'
        if self.s.get('show_version_in_autocomplete_box'):
            if self.s.get('show_library_before_version'):
                method = 'get_library_and_version'
            else:
                method = 'get_version_and_library'
        return method

    def on_post_save(self, view):
        if not is_robot_format(view):
            return
        if not self.keywords_owner.has_data():
            self.keywords_owner.clear_data()
            self._collect_keywords()

    def on_query_completions(self, view, prefix, locations):
        current_file = view.file_name()
        completions = []
        if is_robot_or_txt_file(current_file):
            completions = self.keywords_owner.get_autocomplete_list(prefix)
            completions.sort()
        return completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS


class RobotFrameworkOpenKeywordDocCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(RobotFrameworkOpenKeywordDocCommand, self).__init__(*args, **kwargs)
        self.keywords_owner = RFKeywordAggregateAutoCompleteListAndDefinitions()

    def run(self, edit):
        if not is_robot_format(self.view):
            return
        sel = self.view.sel()[0]
        line = re.compile('\r|\n').split(self.view.substr(self.view.line(sel)))[0]
        row, col = self.view.rowcol(sel.begin())
        keyword = get_keyword_at_pos(line, col)
        if not keyword:
            return
        GoToWebKeywordThread(self.view, self.view.file_name(),
                             self.keywords_owner.get_web_definitions_list(keyword),
                             select_keyword_and_do_action, 'show_definition').start()


class RobotFrameworkFetchKeywordDocCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(RobotFrameworkFetchKeywordDocCommand, self).__init__(*args, **kwargs)
        self.keywords_owner = RFKeywordAggregateAutoCompleteListAndDefinitions()

    def run(self, edit):
        if not is_robot_format(self.view):
            return
        sel = self.view.sel()[0]
        line = re.compile('\r|\n').split(self.view.substr(self.view.line(sel)))[0]
        row, col = self.view.rowcol(sel.begin())
        keyword = get_keyword_at_pos(line, col)
        if not keyword:
            return
        GoToWebKeywordThread(self.view, self.view.file_name(),
                             self.keywords_owner.get_web_definitions_list(keyword),
                             select_keyword_and_do_action, 'insert_doc').start()


class RobotFrameworkReindexPackagesCommand(sublime_plugin.WindowCommand):

    def run(self, *args, **kwargs):
        if not is_robot_format(self.window.active_view()):
            return
        self.s = sublime.load_settings(settings_filename)
        libs_dir = self.s.get('libs_dir')
        if not os.path.exists(libs_dir):
            return sublime.error_message(no_libs_dir(libs_dir))

        RFKeywordCollector()._collect_keywords()