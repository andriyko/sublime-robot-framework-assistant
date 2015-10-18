from os import path
from suite_parser_vars import get_resource_path


def get_variables():
    root_dir = path.dirname(path.abspath(__file__))
    resource_dir = get_resource_path(root_dir)
    var = {}
    var['SCREENSHOT_KW'] = get_screenshot()
    return var


def get_screenshot():
    data = {}
    data['library_module'] = 'Screenshot'
    data['keywords'] = screenshot_keywords()
    return data


def screenshot_keywords():
    kws = {}
    kw = {}
    kw['keyword_name'] = 'Set Screenshot Directory'
    kw['tags'] = []
    kw['documentation'] = 'Sets the directory where screenshots are saved.'
    kw['keyword_arguments'] = ['path']
    kws[kw['keyword_name'].lower().replace(' ', '')] = kw
    kw = {}
    kw['keyword_name'] = 'Take Screenshot'
    kw['tags'] = []
    kw['documentation'] = \
        'Takes a screenshot in JPEG format and embeds it into the log file.'
    kw['keyword_arguments'] = ['name=screenshot', 'width=800px']
    kws[kw['keyword_name'].lower().replace(' ', '')] = kw
    kw = {}
    kw['keyword_name'] = 'Take Screenshot Without Embedding'
    kw['tags'] = []
    kw['documentation'] = 'Takes a screenshot and links it from the log file.'
    kw['keyword_arguments'] = ['name=screenshot']
    kws[kw['keyword_name'].lower().replace(' ', '')] = kw
    return kws
