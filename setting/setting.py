from os import path
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


def get_setting(setting):
    if setting.lower() == 'scanner_dir':
        return SCANNER_DIR
    elif setting.lower() == 'index_dir':
        return INDEX_DIR
    elif setting.lower() == 'scanner_runner':
        return SCANNER_RUNNER
    elif setting.lower() == 'index_runner':
        return INDEX_RUNNER
    elif setting.lower() == 'log_file':
        return LOG_FILE
    else:
        return get_sublime_setting(setting)


def get_sublime_setting(setting):
    plugin_settings = sublime.load_settings(
        'RobotFrameworkDataEditor.sublime-settings')
    return plugin_settings.get(setting)
