#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from rfassistant.external import six
    from urlparse import urlsplit
except ImportError:
    from ..rfassistant.external import six
    from urllib.parse import urlsplit


def url2name(url):
    return os.path.basename(urlsplit(url)[2])


def _check_ext(filename, ext):
    return os.path.splitext(filename)[1].lower() == ext


def is_json_file(filename):
    return _check_ext(filename, '.json')


def is_txt_file(filename):
    return _check_ext(filename, '.txt')


def is_robot_file(filename):
    return _check_ext(filename, '.robot')


def is_robot_or_txt_file(filename):
    return any([is_robot_file(filename), is_txt_file(filename)])


def is_robot_format(view):
    return view.settings().get('syntax').endswith('robot.tmLanguage')
