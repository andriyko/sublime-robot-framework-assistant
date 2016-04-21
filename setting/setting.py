from os import path
from ..command_helper.current_view import VIEW_FILE_NAME
import sublime

settings_dir = path.dirname(path.realpath(__file__))
package_dir = path.realpath(path.join(settings_dir, '..'))
datapraser = path.join(package_dir, 'dataparser')
SCANNER_RUNNER = path.join(datapraser, 'run_scanner.py')
INDEX_RUNNER = path.join(datapraser, 'run_index.py')
DATABASE_DIR = path.join(package_dir, 'database')
SCANNER_DIR = path.join(DATABASE_DIR, 'scanner')
INDEX_DIR = path.join(DATABASE_DIR, 'index')
LOG_FILE = path.join(DATABASE_DIR, 'scan_index.log')
VIEW_PATH = path.join(DATABASE_DIR, 'view_db')
CURRENT_VIEW_PATH = path.join(VIEW_PATH, VIEW_FILE_NAME)


class SettingObject(object):

    table_dir = 'table_dir'
    index_dir = 'index_dir'
    scanner_runner = 'scanner_runner'
    index_runner = 'index_runner'
    log_file = 'log_file'
    python_binary = 'path_to_python'
    workspace = 'robot_framework_workspace'
    extension = 'robot_framework_extension'
    builtin_variables = 'robot_framework_builtin_variables'
    module_search_path = 'robot_framework_module_search_path'
    view_completions = 'view_completions'
    view_path = 'view_path'
    arg_format = 'robot_framework_keyword_argument_format'
    lib_in_xml = 'robot_framework_libraries_in_xml'


def get_setting(setting):
    if setting.lower() == SettingObject.table_dir:
        return SCANNER_DIR
    elif setting.lower() == SettingObject.index_dir:
        return INDEX_DIR
    elif setting.lower() == SettingObject.scanner_runner:
        return SCANNER_RUNNER
    elif setting.lower() == SettingObject.index_runner:
        return INDEX_RUNNER
    elif setting.lower() == SettingObject.log_file:
        return LOG_FILE
    elif setting.lower() == SettingObject.view_completions:
        return CURRENT_VIEW_PATH
    elif setting.lower() == SettingObject.view_path:
        return VIEW_PATH
    else:
        return get_sublime_setting(setting)


def get_sublime_setting(setting):
    plugin_settings = sublime.load_settings(
        'Robot.sublime-settings')
    return plugin_settings.get(setting)
