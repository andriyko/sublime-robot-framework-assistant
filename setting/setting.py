from os import path
import sublime

SETTINGS_DIR = path.dirname(path.realpath(__file__))
PACKAGE_DIR = path.realpath(path.join(SETTINGS_DIR, '..'))
DATABASE_DIR = path.join(PACKAGE_DIR, 'database')
SCANNER_DIR = path.join(DATABASE_DIR, 'scanner')
INDEX_DIR = path.join(DATABASE_DIR, 'index')


def get_setting(setting):
    if setting.lower() == 'scanner_dir':
        return SCANNER_DIR
    elif setting.lower() == 'index_dir':
        return INDEX_DIR
    else:
        return get_sublime_setting(setting)


def get_sublime_setting(setting):
    plugin_settings = sublime.load_settings(
        'RobotFrameworkDataEditor.sublime-settings')
    return plugin_settings.get(setting)
