from os import path
from suite_parser_vars import get_resource_path
import copy
import inspect
import robot.libraries.Screenshot


def get_variables():
    root_dir = path.dirname(path.abspath(__file__))
    resource_dir = get_resource_path(root_dir)
    var = {}
    var['SCREENSHOT_KW'] = get_screenshot()
    var['MYLIBRARY_KW'] = get_mylibrary(resource_dir)
    var['OTHERMYLIBRARY_KW'] = get_othermylibrary(resource_dir)
    var['MYLIBRARY_XML'] = get_mylibrary_xml(var['MYLIBRARY_KW'])
    var['SELENIUM2LIBRARY_KEYS_LIST'] = ['arguments',
                                         'keywords',
                                         'library_module']
    var['ADDCOOKIE_KEYS_LILST'] = ['keyword_name',
                                   'keyword_arguments',
                                   'documentation',
                                   'tags',
                                   'keyword_file']
    var['LIB_FROM_MODULE'] = get_lib_from_module(resource_dir)
    return var


def get_lib_from_module(resource_dir):
    data = {}
    module = 'LibNoClass'
    data['arguments'] = []
    data['library_module'] = module
    f_path = path.normcase(
        path.normpath(
            path.join(
                resource_dir,
                'suite_tree'
            )
        )
    )
    data['file_path'] = path.join(f_path, '{0}{1}'.format(module, '.py'))
    data['file_name'] = '{0}{1}'.format(module, '.py')
    kws = {}
    kw = {}
    kw['keyword_file'] = data['file_path']
    kw['keyword_name'] = 'Library Keyword 1'
    kw['keyword_arguments'] = ['arg1']
    kw['documentation'] = 'library keyword 1 doc'
    kw['tags'] = []
    kws['library_keyword_1'] = kw
    kw = {}
    kw['keyword_file'] = data['file_path']
    kw['keyword_name'] = 'Library Keyword 2'
    kw['keyword_arguments'] = ['arg1', 'arg2']
    kw['documentation'] = 'library keyword 2 doc'
    kw['tags'] = []
    kws['library_keyword_2'] = kw
    data['keywords'] = kws
    return data


def get_mylibrary(resource_dir):
    module = 'MyLibrary'
    data = {}
    data['arguments'] = []
    data['library_module'] = module
    f_path = path.normcase(
        path.normpath(path.join(resource_dir, '..', 'library')))
    data['file_path'] = path.join(f_path, '{0}{1}'.format(module, '.py'))
    data['file_name'] = '{0}{1}'.format(module, '.py')
    kws = {}
    kw = {}
    kw['keyword_file'] = data['file_path']
    kw['keyword_name'] = 'Keyword 2'
    kw['keyword_arguments'] = ['arg2', 'arg3']
    kw['documentation'] = 'kw 2 doc'
    kw['tags'] = []
    kws['keyword_2'] = kw
    kw = {}
    kw['keyword_file'] = data['file_path']
    kw['keyword_name'] = 'Keyword 1'
    kw['keyword_arguments'] = ['arg1']
    kw['documentation'] = 'kw 1 doc'
    kw['tags'] = ['tag1', 'tag2']
    kws['keyword_1'] = kw
    data['keywords'] = kws
    return data


def get_othermylibrary(resource_dir):
    module = 'OtherMyLibrary'
    data = get_mylibrary(resource_dir)
    data['library_module'] = module
    f_path = path.normcase(
        path.normpath(path.join(resource_dir, '..', 'library')))
    data['file_path'] = path.join(f_path, '{0}{1}'.format(module, '.py'))
    data['file_name'] = '{0}{1}'.format(module, '.py')
    data['arguments'] = ['arg111', 'arg222']
    kws = data['keywords']
    tmp_kws = {}
    for kw_key in kws:
        kw = kws[kw_key]
        kw['keyword_file'] = data['file_path']
        tmp_kws[kw_key] = kw
    data['keywords'] = tmp_kws
    return data


def get_mylibrary_xml(data):
    n_data = copy.deepcopy(data)
    n_data['file_path'] = n_data['file_path'].replace('.py', '.xml')
    del n_data['file_name']
    kws = n_data['keywords']
    tmp_kws = {}
    for kw_key in kws:
        kw = kws[kw_key]
        kw['keyword_file'] = None
        tmp_kws[kw_key] = kw
    n_data['keywords'] = tmp_kws
    return n_data


def get_screenshot():
    source_file = inspect.getsourcefile(robot.libraries.Screenshot)
    data = {}
    data['library_module'] = 'Screenshot'
    data['keywords'] = screenshot_keywords(source_file)
    data['arguments'] = []
    return data


def screenshot_keywords(source_file):
    kws = {}
    kw = {}
    kw['keyword_file'] = source_file
    kw['keyword_name'] = 'Set Screenshot Directory'
    kw['tags'] = []
    kw['documentation'] = 'Sets the directory where screenshots are saved.'
    kw['keyword_arguments'] = ['path']
    kws[kw['keyword_name'].lower().replace(' ', '_')] = kw
    kw = {}
    kw['keyword_file'] = source_file
    kw['keyword_name'] = 'Take Screenshot'
    kw['tags'] = []
    kw['documentation'] = \
        'Takes a screenshot in JPEG format and embeds it into the log file.'
    kw['keyword_arguments'] = ['name=screenshot', 'width=800px']
    kws[kw['keyword_name'].lower().replace(' ', '_')] = kw
    kw = {}
    kw['keyword_file'] = source_file
    kw['keyword_name'] = 'Take Screenshot Without Embedding'
    kw['tags'] = []
    kw['documentation'] = 'Takes a screenshot and links it from the log file.'
    kw['keyword_arguments'] = ['name=screenshot']
    kws[kw['keyword_name'].lower().replace(' ', '_')] = kw
    return kws
