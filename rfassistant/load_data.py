#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
import os
import threading
import re

# Plugin imports
try:
    from rfassistant import six
except ImportError:
    from ..rfassistant import six

if six.PY2:
    import console_logging as logging
    from rfassistant.settings import settings
    from rfassistant.items import RFGlobalVars, RFKeywordSource, RFVariable, RFKeyword
    from mixins import is_json_file, is_robot_language_file, is_robot_format, insert_robot_var, is_robot_var
    from utils import Singleton, StaticDataReader, CachedData
    from get_text import get_text_under_cursor, select_item_and_do_action
else:
    from ..rfassistant import console_logging as logging
    from .settings import settings
    from .items import RFGlobalVars, RFKeywordSource, RFVariable, RFKeyword
    from .mixins import is_json_file, is_robot_language_file, is_robot_format, insert_robot_var, is_robot_var
    from .utils import Singleton, StaticDataReader, CachedData
    from .get_text import get_text_under_cursor, select_item_and_do_action


ALLOW_UNPROMPTED_GO_TO = True
logger = logging.getLogger(__name__)


class GoToItemThread(threading.Thread):
    def __init__(self, view, view_file, results, method, action):
        self.view = view
        self.view_file = view_file
        self.results = results
        self.method = method
        self.action = action
        threading.Thread.__init__(self)

    def run(self):
        sublime.set_timeout(lambda: self.method(self.view, self.results, self.action), 50)


class DynamicAutoCompleteListsAndDefinitionsAggregator(six.with_metaclass(Singleton, object)):
    def __init__(self):
        self.autocomplete_keywords = []
        self.autocomplete_variables = []
        self.autocomplete_method = 'get_source'

    def clear_autocomplete(self):
        self.autocomplete_keywords = []

    def has_autocomplete(self):
        return any([self.autocomplete_keywords, self.autocomplete_variables])

    # add data
    def add_kw_for_autocomplete(self, keyword):
        self.autocomplete_keywords.append(keyword)

    def add_var_for_autocomplete(self, var):
        self.autocomplete_variables.append(var)

    # get data
    def _get_kw_info_for_autocomplete(self, kw):
        return kw.name + '\t' + getattr(kw, self.autocomplete_method)(), kw.get_name_and_signature()

    # get autocomplete data for keywords
    def get_keywords_autocomplete_list(self, word):
        return [self._get_kw_info_for_autocomplete(kw) for kw in self.autocomplete_keywords
                if word.lower() in kw.name.lower()]

        # get autocomplete data for vars
    def get_vars_autocomplete_list(self, word):
        return [
            (var.name + '\t' + str(var.source or var.type_), '{0}'.format(insert_robot_var(var.name)))
            for var in self.autocomplete_variables if word.lower() in var.name.lower()
        ]

    # get autocomplete data for all types
    def get_autocomplete_list(self, word):
        if word.startswith('$') or word.startswith('@'):  # scalar($) and list(@) variables
            return self.get_vars_autocomplete_list(word)
        return self.get_keywords_autocomplete_list(word)


class StaticAutoCompleteListsAndDefinitionsAggregator(six.with_metaclass(Singleton, object)):
    def __init__(self):
        self.autocomplete_keywords = []
        self.autocomplete_sources = []
        self.autocomplete_variables = []
        self.definitions_keywords = {}
        self.definitions_sources = {}
        self.definitions_variables = {}
        self._autocomplete_method = 'get_source_name'

    @property
    def autocomplete_method(self):
        return self._autocomplete_method

    @autocomplete_method.setter
    def autocomplete_method(self, method):
        allowed_methods = ('get_source', 'get_source_name')
        if method not in allowed_methods:
            raise ValueError(
                'Invalid method for autocomplete: {0}. Must be one from: {1}'.format(method, ', '.join(allowed_methods))
            )
        self._autocomplete_method = method

    def clear_autocomplete(self):
        self.autocomplete_keywords = []
        self.autocomplete_sources = []
        self.autocomplete_variables = []

    def clear_definitions(self):
        self.definitions_keywords = {}
        self.definitions_sources = {}
        self.definitions_variables = {}

    def clear_data(self):
        self.clear_autocomplete()
        self.clear_definitions()

    def has_autocomplete(self):
        return any([self.autocomplete_keywords, self.autocomplete_sources, self.autocomplete_variables])

    def has_definitions(self):
        return any([self.definitions_keywords, self.definitions_sources, self.definitions_variables])

    def has_data(self):
        return all([self.has_autocomplete(), self.has_definitions()])

    # add data
    def add_kw_for_autocomplete(self, keyword):
        self.autocomplete_keywords.append(keyword)

    def add_kw_for_definitions(self, keyword):
        self.definitions_keywords.setdefault(keyword.name, set()).add(keyword)

    def add_source_for_definitions(self, source):
        self.definitions_sources.setdefault(source.name, set()).add(source)

    def add_source_for_autocomplete(self, source):
        self.autocomplete_sources.append(source)

    def add_var_for_autocomplete(self, var):
        self.autocomplete_variables.append(var)

    def add_var_for_definitions(self, var):
        self.definitions_variables.setdefault(var.name, set()).add(var)

    def add_builtin_vars_for_autocomplete_and_definitions_lists(self):
        for var_name, var_value in RFGlobalVars.variables.items():
            var = RFVariable(source=None, name=var_name, value=var_value)
            self.add_var_for_autocomplete(var)
            self.add_var_for_definitions(var)

    # get data
    def _get_kw_info_for_autocomplete(self, kw):
        return kw.name + '\t' + getattr(kw, self.autocomplete_method)(), kw.get_name_and_signature()

    # get autocomplete data for keywords
    def get_keywords_autocomplete_list(self, word, name_of_source=None):
        if name_of_source:
            name_of_source = name_of_source.lower()
            # only name of library is given and autocomplete is triggered after dot character.
            # BuiltIn.
            if word == '':
                return [self._get_kw_info_for_autocomplete(kw) for kw in self.autocomplete_keywords
                        if kw.source.name.lower() == name_of_source]
                # name of library and part of keyword name are given
            # BuiltIn.Call
            return [self._get_kw_info_for_autocomplete(kw) for kw in self.autocomplete_keywords
                    if word.lower() in kw.name.lower() and kw.source.name.lower() == name_of_source]
            # only part of keyword name is given
        return [self._get_kw_info_for_autocomplete(kw) for kw in self.autocomplete_keywords
                if word.lower() in kw.name.lower()]

    # get autocomplete data for keywords parents (sources)
    def get_sources_autocomplete_list(self, word):
        return [
            (source.name + '\t' + str(source), source.name)
            for source in self.autocomplete_sources if word.lower() in source.name.lower()
        ]

    # get autocomplete data for vars
    def get_vars_autocomplete_list(self, word):
        return [
            (var.name + '\t' + str(var.source or var.type_), '{0}'.format(insert_robot_var(var.name)))
            for var in self.autocomplete_variables if word.lower() in var.name.lower()
        ]

    # get autocomplete data for all types
    def get_autocomplete_list(self, word, name_of_source=None):
        autocomplete_list = []
        keywords = self.get_keywords_autocomplete_list(word, name_of_source=name_of_source)
        if name_of_source:
            return keywords
        variables = self.get_vars_autocomplete_list(word)
        if word.startswith('$') or word.startswith('@'):  # scalar($) and list(@) variables
            return variables
        sources = self.get_sources_autocomplete_list(word)
        autocomplete_list.extend(keywords)
        autocomplete_list.extend(sources)
        return autocomplete_list

    # get definitions
    def get_keywords_definitions_list(self, word, name_of_source=None):
        definitions_list = []
        if name_of_source:
            if word in self.definitions_keywords:
                candidates = [candidate for candidate in self.definitions_keywords[word]
                              if candidate.source.name.lower() == name_of_source.lower()]
                definitions_list.extend(candidates)
        elif word in self.definitions_keywords:
            definitions_list.extend(self.definitions_keywords[word])
        return definitions_list

    def get_filtered_keywords_definitions_list(self, word, name_of_source=None, filter_by_attrs=()):
        keywords = self.get_keywords_definitions_list(word, name_of_source=name_of_source)
        if not filter_by_attrs:
            return keywords
        return [kw for kw in keywords if any([getattr(kw, attr, None) for attr in filter_by_attrs])]

    def get_sources_definitions_list(self, word):
        definitions_list = []
        if word in self.definitions_sources:
            definitions_list.extend(self.definitions_sources[word])
        return definitions_list

    def get_vars_definitions_list(self, word):
        definitions_list = []
        if word in self.definitions_variables:
            definitions_list.extend(self.definitions_variables[word])
        return definitions_list


class RFDynamicDataCollectorThread(threading.Thread):
    def __init__(self, collector, fname, timeout_seconds=30):
        self.view = sublime.active_window().active_view()
        self.collector = collector
        self.timeout = timeout_seconds
        self.status_name = 'rf_collector'
        self.fname = fname
        threading.Thread.__init__(self)

    def _get_keyword_source_from_data(self, data):
        _get = lambda key: data.get(key, None)
        return RFKeywordSource(library=_get('library'), version=_get('version'), resource=_get('resource'),
                               path=_get('path'), url=_get('url'), noauth_url=_get('noauth_url'))

    def _get_keywords_from_data(self, data):
        for kw in data['keywords']:
            yield RFKeyword(None, name=kw['name'], arguments=kw['arguments'],
                            documentation=kw.get('documentation', None), path=kw.get('path', None))

    def _get_variables_from_data(self, data):
        for var in data.get('variables', ()):
            yield RFVariable(source=None, name=var['name'], value=var['value'])

    def collect_data_lists(self, data):
        if not data:
            return
        for keyword in self._get_keywords_from_data(data):
            self.collector.autocomplete_dynamic_owner.add_kw_for_autocomplete(keyword)
        for variable in self._get_variables_from_data(data):
            self.collector.autocomplete_dynamic_owner.add_var_for_autocomplete(variable)
        sublime.set_timeout(lambda: self.view.erase_status(self.status_name), 100)

    def run(self):
        try:
            self.collect_data_lists(CachedData().get_file(self.fname))
        except IOError as err:
            logger.debug(err)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class RFStaticDataCollectorThread(threading.Thread):
    def __init__(self, collector, data_lookup_dirs=(), timeout_seconds=30):
        self.view = sublime.active_window().active_view()
        self.collector = collector
        self.timeout = timeout_seconds
        self.data_lookup_dirs = data_lookup_dirs
        self.status_name = 'rf_collector'
        threading.Thread.__init__(self)

    def _get_json_files(self, base_dir, dir_name, *args):
        files_list = []
        d = os.path.join(base_dir, dir_name)
        if not os.path.isdir(d):
            return files_list
        for f in os.listdir(d):
            dirfile = os.path.join(d, f)
            if os.path.isfile(dirfile):
                if is_json_file(dirfile):
                    files_list.append(dirfile)
            elif os.path.isdir(dirfile):
                files_list += self._get_json_files(base_dir, dirfile, *args)
        return files_list

    def _get_keyword_source_from_data(self, data):
        _get = lambda key: data.get(key, None)
        # 'path' is also optional for rfdocs source type.
        return RFKeywordSource(library=_get('library'), version=_get('version'), resource=_get('resource'),
                               path=_get('path'), url=_get('url'), noauth_url=_get('noauth_url'))

    def _get_keywords_from_data(self, source, data):
        for kw in data['keywords']:
            #documentation  and kw_path are optional for rfdocs
            yield RFKeyword(source, name=kw['name'], arguments=kw['arguments'],
                            documentation=kw.get('documentation', None), path=kw.get('path', None))

    def _get_variables_from_data(self, source, data):
        for var in data.get('variables', ()):
            yield RFVariable(source=source, name=var['name'], value=var['value'])

    def collect_data_lists(self, data):
        source = self._get_keyword_source_from_data(data)
        self.collector.autocomplete_owner.add_source_for_definitions(source)
        self.collector.autocomplete_owner.add_source_for_autocomplete(source)
        for keyword in self._get_keywords_from_data(source, data):
            self.collector.autocomplete_owner.add_kw_for_autocomplete(keyword)
            self.collector.autocomplete_owner.add_kw_for_definitions(keyword)
        for variable in self._get_variables_from_data(source, data):
            self.collector.autocomplete_owner.add_var_for_autocomplete(variable)
            self.collector.autocomplete_owner.add_var_for_definitions(variable)
        sublime.set_timeout(lambda: self.view.erase_status(self.status_name), 100)

    def run(self):
        self.collector.autocomplete_owner.add_builtin_vars_for_autocomplete_and_definitions_lists()
        for d in self.data_lookup_dirs:
            for folder in os.listdir(d):
                json_files = self._get_json_files(d, folder)
                for file_name in json_files:
                    sublime.set_timeout(
                        lambda: self.view.set_status(self.status_name,
                                                     'Loading data from: {0}'.format(os.path.basename(file_name))), 100
                    )
                    data = StaticDataReader.get_data(file_name)
                    self.collect_data_lists(data)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class RFDataCollector(sublime_plugin.EventListener):

    _collector_thread = None

    def __init__(self, *args, **kwargs):
        global settings
        super(RFDataCollector, self).__init__(*args, **kwargs)
        if six.PY2:
            setattr(self, 'on_load', self._on_load)
        else:
            setattr(self, 'on_load_async', self._on_load)
            setattr(self, 'on_activated', self._on_activated)
        self.autocomplete_owner = StaticAutoCompleteListsAndDefinitionsAggregator()
        self.autocomplete_dynamic_owner = DynamicAutoCompleteListsAndDefinitionsAggregator()

    def get_method_for_autocomplete(self):
        method = 'get_source_name'
        if settings.show_version_in_autocomplete_box:
            method = 'get_source'
        return method

    def collect_dynamic_data(self, file_with_data):
        self.autocomplete_dynamic_owner.clear_autocomplete()
        if self._collector_thread is not None:
            self._collector_thread.stop()
            self._collector_thread = RFDynamicDataCollectorThread(self, file_with_data, timeout_seconds=30)
            self._collector_thread.start()

    def collect_data(self):
        rfdocs_dir = str(settings.rfdocs_dir)
        python_libs_dir = str(settings.python_libs_dir)
        resources_dir = str(settings.resources_dir)
        if not any([os.path.exists(p) for p in [rfdocs_dir, python_libs_dir, resources_dir, ]]):
            return
        self.autocomplete_owner.autocomplete_method = self.get_method_for_autocomplete()
        self.autocomplete_owner.clear_data()
        if self._collector_thread is not None:
            self._collector_thread.stop()
        self._collector_thread = \
            RFStaticDataCollectorThread(self,
                                        data_lookup_dirs=[rfdocs_dir, python_libs_dir, resources_dir],
                                        timeout_seconds=30)
        self._collector_thread.start()

    def _on_load(self, view):
        if not is_robot_format(view):
            return
        if self.autocomplete_owner.has_data():
            return
        self.collect_data()

    def _on_activated(self, view):
        if not is_robot_format(view):
            return
        if self.autocomplete_owner.has_data():
            return
        self.collect_data()

    def on_post_save(self, view):
        if not is_robot_format(view):
            return
            # if not self.autocomplete_dynamic_owner.has_autocomplete():
        #     self.collect_dynamic_data(view.file_name())
        self.collect_dynamic_data(view.file_name())
        if not self.autocomplete_owner.has_data():
            self.autocomplete_owner.clear_data()
            self.collect_data()

    def on_query_completions(self, view, prefix, operand):
        completions = []
        name_of_source = None
        if not is_robot_language_file(view.file_name(), settings.associated_file_extensions):
            return completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS
            # ignore 'prefix' argument, instead get text under cursor using custom method
        text_under_cursor = get_text_under_cursor(view)
        if not text_under_cursor:
            return completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS
        result = re.split('\.', text_under_cursor, maxsplit=1)
        if len(result) == 2:
            name_of_source = result[0]
            text_under_cursor = result[1]
        completions = self.autocomplete_owner.get_autocomplete_list(text_under_cursor, name_of_source=name_of_source)
        completions_dynamic = self.autocomplete_dynamic_owner.get_autocomplete_list(text_under_cursor)
        completions.extend(completions_dynamic)

        # The event listeners works for every file in scope(for all opened .txt and .robot files)
        # in a separate thread, thus result may have duplicates.
        # Clean it.
        completions = list(set(completions))
        completions.sort()
        return completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS


# commands
class RobotFrameworkBaseRunCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        super(RobotFrameworkBaseRunCommand, self).__init__(*args, **kwargs)
        self.autocomplete_owner = StaticAutoCompleteListsAndDefinitionsAggregator()

    def run(self, edit):
        if not is_robot_format(self.view):
            return
        name_of_source = None
        text_under_cursor = get_text_under_cursor(self.view)
        result = re.split('\.', text_under_cursor, maxsplit=1)
        if len(result) == 2:
            name_of_source = result[0]
            text_under_cursor = result[1]
        if not text_under_cursor:
            return
        self.go_to_item_thread(text_under_cursor, name_of_source=name_of_source)

    def go_to_item_thread(self, text_under_cursor, name_of_source=None):
        raise NotImplementedError('Must be implemented in subclass')


class RobotFrameworkOpenItemDocCommand(RobotFrameworkBaseRunCommand):
    def go_to_item_thread(self, word, name_of_source=None):
        sources = self.autocomplete_owner.get_sources_definitions_list(word)
        filtered_items = \
            self.autocomplete_owner.get_filtered_keywords_definitions_list(word,
                                                                           name_of_source=name_of_source,
                                                                           filter_by_attrs=('external_url',))
        filtered_items.extend(sources)
        GoToItemThread(self.view, self.view.file_name(),
                       filtered_items,
                       select_item_and_do_action, 'show_doc_in_browser').start()


class RobotFrameworkLogItemCommand(RobotFrameworkBaseRunCommand):
    def go_to_item_thread(self, word, name_of_source=None):
        if is_robot_var(word):
            filtered_items = self.autocomplete_owner.get_vars_definitions_list(word)
        else:
            filtered_items = self.autocomplete_owner.\
                get_filtered_keywords_definitions_list(word,
                                                       name_of_source=name_of_source,
                                                       filter_by_attrs=('rfdocs_url', 'documentation',))
        GoToItemThread(self.view, self.view.file_name(),
                       filtered_items,
                       select_item_and_do_action, 'show_doc_in_editor').start()


class RobotFrameworkGoToItemSourceCommand(RobotFrameworkBaseRunCommand):
    def go_to_item_thread(self, word, name_of_source=None):
        if is_robot_var(word):
            filtered_items = self.autocomplete_owner.get_vars_definitions_list(word)
        else:
            # try to get sources(keywords parents - either python libraries or resources)
            sources = self.autocomplete_owner.get_sources_definitions_list(word)
            filtered_items = \
                self.autocomplete_owner.get_filtered_keywords_definitions_list(word,
                                                                               name_of_source=name_of_source,
                                                                               filter_by_attrs=('path',))
            filtered_items.extend(sources)
        GoToItemThread(self.view, self.view.file_name(),
                       filtered_items,
                       select_item_and_do_action, 'goto_source').start()


class RobotFrameworkRecollectDataCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        if not is_robot_format(self.window.active_view()):
            return
        RFDataCollector().collect_data()


class RobotFrameworkScanCurrentFileCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        view = self.window.active_view()
        if not is_robot_format(view):
            return
        CachedData().init()
        view.run_command('robot_framework_scan_test_case_files', {'file_to_read': view.file_name()})
