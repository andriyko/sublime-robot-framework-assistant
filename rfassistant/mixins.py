#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Python imports
import hashlib
import re
import os
import time

# Plugin imports
try:
    from rfassistant.external import six
except ImportError:
    from ..rfassistant.external import six

if six.PY2:
    from urlparse import urlsplit
else:
    from urllib.parse import urlsplit
    from functools import reduce

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


def is_robot_var(string):
    if not isinstance(string, basestring):
        return False
    length = len(string)
    return length > 3 and string[0] in ['$', '@', ] and string.rfind('{') == 1 and string.find('}') == length - 1


def is_scalar_var(string):
    return is_robot_var(string) and string[0] == '$'


def is_list_var(string):
    return is_robot_var(string) and string[0] == '@'


def escape_robot_var(var):
    return re.sub('([${}])', r'\\\1', var)


def insert_robot_var(var):
    return re.sub('([$@])', r'', var)


def timeit(method):

    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        print('%r (%r, %r) %2.2f milliseconds' % (method.__name__, args, kwargs, (te-ts) * 1000))
        return result

    return timed


def logit(method):

    def logit(*args, **kwargs):
        result = method(*args, **kwargs)
        print('method=%r, args=%r, kwargs=%r, result=%r' % (method.__name__, args, kwargs, result))
        return result

    return logit


def url2name(url):
    return os.path.basename(urlsplit(url)[2])


def _check_ext(filename, ext):
    return os.path.splitext(filename)[1].lower() == ext if filename else False


def is_json_file(filename):
    return _check_ext(filename, '.json')


def is_txt_file(filename):
    return _check_ext(filename, '.txt')


def is_python_file(filename):
    return _check_ext(filename, '.py')


def is_robot_file(filename):
    return _check_ext(filename, '.robot')


def is_robot_or_txt_file(filename):
    return os.path.splitext(filename)[1].lower() in ['.robot', '.txt'] if filename else False


def is_robot_format(view):
    return view.settings().get('syntax').endswith('robot.tmLanguage')


def getattr_consecutive(obj, dot_notated_string):
    """
    Allows dot-notated strings to be passed to `getattr`
    """
    return reduce(getattr, dot_notated_string.split('.'), obj)


def def_name_to_keyword(name):
    name = name.replace('_', ' ').strip()
    return name.title() if name.islower() else name


def keyword_to_def_name(name):
    name = name.replace(' ', '_').strip()
    return name.lower()


def calculate_checksum(f):
    if not os.path.exists(f):
        return None
    with open(f) as f_obj:
        md5_checksum = hashlib.md5(f_obj.read()).hexdigest()
    return md5_checksum
