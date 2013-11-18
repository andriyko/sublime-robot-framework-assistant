#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import ast
import json
import os
import shutil

try:
    from rfassistant.external import six
    from rfassistant import settings_filename, no_manifest_file, \
        libs_manifest_path, libs_dir_path, libs_update_url_default
    from rfassistant.downloader.donwloader import PackageDownloader, ManifestDownloader
    from rfassistant.external.html2text import html2text
except ImportError:
    from ...rfassistant.external import six
    from ...rfassistant import settings_filename, no_manifest_file, \
        libs_manifest_path, libs_dir_path, libs_update_url_default
    from ..downloader.donwloader import PackageDownloader, ManifestDownloader
    from ..external.html2text import html2text

try:
    import ssl
except (ImportError):
    pass


class RobotFrameworkFetchKeywordIntoViewCommand(sublime_plugin.TextCommand):
    result = None
    url = None

    def run(self, edit, url):
        self.url = url
        self.status_name = 'rf_doc_fetcher'
        thread = ManifestDownloader(url, 5)
        thread.start()
        thread.join()
        self.handle_thread(edit, thread)

    def _insert_text(self, edit, txt):
        region = self.view.sel()[0]
        line = self.view.line(region)
        evaluated = ast.literal_eval(txt)
        text_from_html = html2text(evaluated['documentation'])
        self.view.insert(edit, line.begin(), "\n{0}\n".format(text_from_html))

    def handle_thread(self, edit, thread):
        self.view.set_status(self.status_name, 'Fetching data from URL: {0}'.format(self.url))
        txt = thread.txt
        status = thread.result
        self.view.erase_status(self.status_name)
        if not status:
            return sublime.error_message('Failed to fetch data from URL: {0}'.format(self.url))
        self._insert_text(edit, txt)
        sublime.status_message('Fetched data from URL: {0}'.format(self.url))


class RobotFrameworkFetchManifestCommand(sublime_plugin.TextCommand):
    result = None
    url = None
    location = None

    def run(self, edit, url, location=None):
        self.url = url
        self.location = location

        threads = []
        thread = ManifestDownloader(url, 5)
        threads.append(thread)
        thread.start()
        self.handle_threads(edit, threads)

    def handle_threads(self, edit, threads, offset=0, i=0, d=1):
        status_name = 'rf_manifest_fetcher'
        status = None
        txt = ''
        next_threads = []
        for thread in threads:
            status = thread.result
            txt = thread.txt
            if thread.is_alive():
                next_threads.append(thread)
                continue
            if thread.result is False:
                continue

        threads = next_threads

        if len(threads):
            # This animates a little activity indicator in the status area
            before = i % 8
            after = 7 - before
            if not after:
                d = -1
            if not before:
                d = 1
            i += d
            self.view.set_status(status_name,
                                 'Downloading file from {0} [{1}={2}] '.format(self.url, ' ' * before, ' ' * after))
            sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, d), 100)
            return
        self.view.erase_status(status_name)
        if status:
            with open(self.location, 'w') as f:
                f.write(txt)
            sublime.status_message('The file was successfully downloaded from {0}'.format(self.url))


class RobotFrameworkFetchPackageCommand(sublime_plugin.TextCommand):
    result = None
    url = None
    location = None

    def run(self, edit, url, location=None):
        self.url = url
        self.location = location

        threads = []
        thread = PackageDownloader(url, location, 5)
        threads.append(thread)
        thread.start()
        self.handle_threads(edit, threads)

    def handle_threads(self, edit, threads, offset=0, i=0, d=1):
        status_name = 'rf_packager_fetcher'
        status = None
        next_threads = []
        for thread in threads:
            status = thread.result
            if thread.is_alive():
                next_threads.append(thread)
                continue
            if thread.result is False:
                continue

        threads = next_threads

        if len(threads):
            # This animates a little activity indicator in the status area
            before = i % 8
            after = 7 - before
            if not after:
                d = -1
            if not before:
                d = 1
            i += d
            self.view.set_status(status_name,
                                 'Downloading file from {0} [{1}={2}] '.format(self.url, ' ' * before, ' ' * after))
            sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, d), 100)
            return

        self.view.erase_status(status_name)
        if status:
            sublime.status_message('The file was successfully downloaded from {0}'.format(self.url))


class RobotFrameworkDownloadManifestCommand(sublime_plugin.WindowCommand):
    s = None
    libs_update_url_placeholder = libs_update_url_default
    libs_manifest_placeholder = libs_manifest_path
    libs_dir_placeholder = libs_dir_path
    show_version_in_autocomplete_box = False

    def run(self, *args, **kwargs):
        self.s = sublime.load_settings(settings_filename)
        update_url = self._get_prop_or_set_default('libs_update_url', self.libs_update_url_placeholder)
        libs_manifest = self._get_prop_or_set_default('libs_manifest', self.libs_manifest_placeholder)
        self.window.run_command("robot_framework_fetch_manifest", {"location": libs_manifest, "url": update_url})

    def _get_prop_or_set_default(self, prop, placeholder):
        val = self.s.get(prop)
        if not val:
            self.s.set(prop, placeholder)
            sublime.save_settings(settings_filename)
            val = self.s.get(prop)
        return val


class RobotFrameworkDownloadPackagesCommand(sublime_plugin.WindowCommand):
    s = None

    def run(self, *args, **kwargs):
        self.s = sublime.load_settings(settings_filename)
        libs_manifest = self.s.get('libs_manifest')
        if not os.path.exists(libs_manifest):
            sublime.error_message(no_manifest_file(libs_manifest))
            return
        libs_dir = self.s.get('libs_dir')
        if os.path.exists(libs_dir):
            shutil.rmtree(libs_dir)
            os.makedirs(libs_dir)
        else:
            os.makedirs(libs_dir)
        with open(libs_manifest, 'r') as f:
            content = json.load(f)
        for item in content:
            item_url = item['url']
            if item_url:
                self.window.run_command("robot_framework_fetch_package", {"location": libs_dir, "url": item_url})

    def _get_prop_or_set_default(self, prop, placeholder):
        val = self.s.get(prop)
        if not val:
            self.s.set(prop, placeholder)
            sublime.save_settings(settings_filename)
            val = self.s.get(prop)
        return val