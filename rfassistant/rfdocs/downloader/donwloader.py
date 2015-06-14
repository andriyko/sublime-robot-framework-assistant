#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime

# Python imports
import json
import os
import re
import threading

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ....rfassistant import PY2

if PY2:
    import urllib2 as url_request
    from rfassistant import user_agent, mkdir_safe, package_dir

    url_request_http_error = url_request.HTTPError
    url_request_url_error = url_request.URLError
    str_or_unicode = unicode
else:
    import urllib.request as url_request
    import urllib.error as url_error
    from ....rfassistant import user_agent, mkdir_safe, package_dir

    url_request_http_error = url_error.HTTPError
    url_request_url_error = url_error.URLError
    str_or_unicode = str


def is_safe_name(name):
    regex = '[\x00-\x1F\x7F-\xFF]'
    if any([name[0] == '/', name.find('..') != -1, name.find('~') != -1,
            re.search(regex, name) is not None]):
        sublime.error_message('{0}: Unsafe name. Aborted.'.format(__name__))
        return False
    return True


class Requestor(object):
    headers = {'User-Agent': user_agent, 'Accept': 'application/json; indent=2',
               'Content-Type': 'application/json'}

    def __init__(self, url, timeout, headers={}):
        self.url = url
        self.timeout = timeout
        self.headers.update(headers)

    def get_response(self):
        request = url_request.Request(self.url, headers=self.headers)
        response = url_request.urlopen(request, timeout=self.timeout)
        return response


class ManifestDownloader(threading.Thread):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = int(timeout)
        self.result = None
        self.txt = None
        threading.Thread.__init__(self)

    def run(self):
        self.download_data()

    def download_data(self):
        try:
            response = Requestor(self.url, self.timeout).get_response()
            self.txt = str_or_unicode(response.read(), 'utf-8')
            self.result = True
        except (url_request_http_error, url_request_url_error) as e:
            self.result = False
            err = '{0}: Error contacting server: {1}'.format(__name__, e.reason)
            sublime.error_message(err)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class LibraryDownloader(threading.Thread):
    def __init__(self, url, location, slug, timeout):
        self.url = url
        self.slug = slug
        self.location = location
        self.timeout = int(timeout)
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        self.download_data()

    def download_data(self):
        if not is_safe_name(self.slug):
            return False
        item_location = os.path.join(self.location, '{}.json'.format(self.slug))
        try:
            response = Requestor(self.url, self.timeout).get_response()
            with open(item_location, 'w') as f:
                f.write(response.read().decode("utf-8"))
            self.result = True
            return
        except (url_request_http_error, url_request_url_error) as e:
            self.result = False
            err = '{0}: Error contacting server: {0}'.format(__name__, e.reason)
            sublime.error_message(err)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class PackageDownloader(threading.Thread):
    def __init__(self, url, location, slug, timeout):
        self.url = url
        self.slug = slug
        self.location = location
        self.timeout = int(timeout)
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        self.download_data()

    def download_data(self):
        if not is_safe_name(self.slug):
            return False
        package_location = os.path.join(self.location, self.slug)
        try:
            response = Requestor(self.url, self.timeout).get_response()
            mkdir_safe(package_location, package_dir)
            for item in json.loads(response.read().decode("utf-8"))['versions']:
                LibraryDownloader(item['url'], package_location, item['name'], self.timeout).run()
            self.result = True
            return
        except (url_request_http_error, url_request_url_error) as e:
            self.result = False
            err = '{0}: Error contacting server: {0}'.format(__name__, e.reason)
            sublime.error_message(err)
            if package_location is not None and os.path.exists(package_location):
                os.remove(package_location)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()
