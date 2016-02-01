import os
import fnmatch


def finder(path, ext):
    """Returns files from path by extension"""
    l = []
    if not ext.startswith('*.'):
        ext = '*.{0}'.format(ext)
    for path, dirs, files in os.walk(os.path.abspath(path)):
        for f in fnmatch.filter(files, ext):
            l.append(os.path.join(path, f))
    return l
