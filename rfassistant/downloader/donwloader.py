#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime

import os
import re
import sys
import threading
import zipfile

try:
    import urllib2 as url_request

    from rfassistant.downloader.cli_downloader import CliDownloader
    from rfassistant import tmp_dir_path
    from rfassistant.mixins import url2name

    url_request_http_error = url_request.HTTPError
    url_request_url_error = url_request.URLError
    str_or_unicode = unicode
except ImportError:
    import urllib.request as url_request
    import urllib.error as url_error

    from ...rfassistant import tmp_dir_path
    from ..downloader.cli_downloader import CliDownloader
    from ..mixins import url2name

    url_request_http_error = url_error.HTTPError
    url_request_url_error = url_error.URLError
    str_or_unicode = str

try:
    import ssl
except ImportError:
    pass


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
            downloaded = False
            if 'ssl' in sys.modules:
                request = url_request.Request(self.url)
                http_file = url_request.urlopen(request, timeout=self.timeout)
                self.txt = str_or_unicode(http_file.read(), 'utf-8')
                downloaded = True
            else:
                clidownload = CliDownloader()
                if clidownload.find_binary('wget'):
                    command = [clidownload.find_binary('wget'),
                               '--connect-timeout={0}'.format(self.timeout), self.url, '-qO-']
                    self.txt = str_or_unicode(clidownload.execute(command), 'utf-8')
                    downloaded = True
                elif clidownload.find_binary('curl'):
                    command = [clidownload.find_binary('curl'),
                               '--connect-timeout', str(self.timeout), '-L', '-sS', self.url]
                    self.txt = str_or_unicode(clidownload.execute(command), 'utf-8')
                    downloaded = True

            if not downloaded:
                sublime.error_message('Unable to download {0} due to no ssl module available '
                                      'and no capable program found. Please install curl or wget.'.format(self.url))
                return False
            else:
                self.result = True

        except (url_request_http_error, url_request_url_error) as e:
            err = '{0}: Error contacting server: {1}'.format(__name__, e.reason)
            sublime.error_message(err)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()


class PackageDownloader(threading.Thread):
    def __init__(self, url, location, timeout):
        self.url = url
        self.location = location
        self.timeout = int(timeout)
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        if not os.path.exists(tmp_dir_path):
            os.makedirs(tmp_dir_path)
        self.download_data()

    def is_safe_name(self):
        name = url2name(self.url)
        regex = '[\x00-\x1F\x7F-\xFF]'
        if name[0] == '/' or name.find('..') != -1 or name.find('~') != -1 or re.search(regex, name) is not None:
            sublime.error_message('{0}: Unable to extract package due to unsafe archive filename.'.format(__name__))
            return False
        return True

    def download_data(self):
        downloaded = False
        if not self.is_safe_name():
            return False
        finalLocation = None
        try:
            finalLocation = os.path.join(tmp_dir_path, url2name(self.url))
            if 'ssl' in sys.modules:
                url_request.install_opener(url_request.build_opener(url_request.ProxyHandler()))
                request = url_request.Request(self.url)
                response = url_request.urlopen(request, timeout=self.timeout)
                output = open(finalLocation, 'wb')
                output.write(response.read())
                output.close()
                downloaded = True
            else:
                clidownload = CliDownloader()
                if clidownload.find_binary('wget'):
                    command = [clidownload.find_binary('wget'),
                               '--connect-timeout={0}'.format(self.timeout), '-O', finalLocation, self.url]
                    clidownload.execute(command)
                    downloaded = True
                elif clidownload.find_binary('curl'):
                    command = [clidownload.find_binary('curl'),
                               '--connect-timeout', str(self.timeout), '-L', self.url, '-o', finalLocation]
                    clidownload.execute(command)
                    downloaded = True

            if not downloaded:
                sublime.error_message('Unable to download {0} due to no ssl module available and no capable'
                                      ' program found. Please install curl or wget.'.format(self.url))
                return False

            else:
                pkg = zipfile.ZipFile(finalLocation, 'r')

                for path in pkg.namelist():
                    if path[0] == '/' or path.find('..') != -1 or path.find('~') != -1:
                        sublime.error_message('{0}: Unable to extract package due to unsafe '
                                              'filename on one or more files.'.format(__name__))
                        return False
                pkg.extractall(self.location)
                pkg.close()
                if os.path.exists(finalLocation):
                    os.remove(finalLocation)
                self.result = True
            return

        except (url_request_http_error, url_request_url_error) as e:
            err = '{0}: Error contacting server: {0}'.format(__name__, e.reason)
        finally:
            if finalLocation is not None and os.path.exists(finalLocation):
                os.remove(finalLocation)
        sublime.error_message(err)
        self.result = False

    def stop(self):
        if self.isAlive():
            self._Thread__stop()