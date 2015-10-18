from os import path
from robot.libdocpkg.robotbuilder import LibraryDocBuilder


def get_variables():
    root_dir = path.dirname(path.abspath(__file__))
    resource_dir = get_resource_path(root_dir)
    var = {}
    var['SCREENSHOT_KW'] = get_screenshot()
    return var


def get_screenshot():
    data = {}
    data['library_module'] = 'Screenshot'

    l = LibraryDocBuilder()
    libdoc = l.build('Screenshot')
    kws = {}
    for kw in libdoc.keywords:
        kw = {}
        kw['keyword_name'] = kw.name
        kw['keyword_arguments'] = kw.args
        kw['documentation'] = kw.doc
        #print kw.tags

