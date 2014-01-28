#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime
import sublime_plugin

# Python imports
import ast
import json
import os
import shutil

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ....rfassistant import PY2

try:
    import ssl
except ImportError:
    pass

if PY2:
    from rfassistant.utils import WriteToPanel
    from rfassistant import no_manifest_file
    from rfassistant.settings import settings
    from rfassistant.rfdocs.downloader.donwloader import PackageDownloader, ManifestDownloader
    from rfassistant.external.html2text import html2text
else:
    from ...utils import WriteToPanel
    from ....rfassistant import no_manifest_file
    from ...settings import settings
    from ..downloader.donwloader import PackageDownloader, ManifestDownloader
    from ...external.html2text import html2text


class RobotFrameworkFetchKeywordIntoViewCommand(sublime_plugin.TextCommand):
    result = None
    url = None

    def run(self, edit, name, url):
        self.name = name
        self.url = url
        self.status_name = 'rf_doc_fetcher'
        thread = ManifestDownloader(url, 5)
        thread.start()
        thread.join()
        self.handle_thread(edit, thread)

    def handle_thread(self, edit, thread):
        self.view.set_status(self.status_name, 'Fetching data from URL: {0}'.format(self.url))
        txt = thread.txt
        status = thread.result
        self.view.erase_status(self.status_name)
        if not status:
            return sublime.error_message('Failed to fetch data from URL: {0}'.format(self.url))
        evaluated = ast.literal_eval(txt)
        text_from_html = html2text(evaluated['documentation'])
        heading = "{0:{1}^80}".format(self.name, "-")
        msg = '\n{heading}\n{body}\n{footer}'.format(heading=heading, body=text_from_html, footer='-'*80)
        WriteToPanel(self.view)(msg)
        sublime.status_message('Fetched data from URL: {0}'.format(self.url))


class RobotFrameworkFetchManifestCommand(sublime_plugin.TextCommand):
    result = None
    url = None
    location = None

    def run(self, edit, url, location=None):
        self.url = url
        self.location = location

        threads = []
        thread = ManifestDownloader(url, 15)
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
        thread = PackageDownloader(url, location, 15)
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

    def run(self, *args, **kwargs):
        self.window.run_command("robot_framework_fetch_manifest",
                                {
                                    "location": settings.rfdocs_manifest,
                                    "url": settings.rfdocs_update_url
                                })


class RobotFrameworkDownloadPackagesCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        rfdocs_manifest = settings.rfdocs_manifest
        if not os.path.exists(rfdocs_manifest):
            sublime.error_message(no_manifest_file(rfdocs_manifest))
            return
        rfdocs_dir = settings.rfdocs_dir
        if os.path.exists(rfdocs_dir):
            shutil.rmtree(rfdocs_dir)
            os.makedirs(rfdocs_dir)
        else:
            os.makedirs(rfdocs_dir)
        with open(rfdocs_manifest, 'r') as f:
            content = json.load(f)
        for item in content:
            item_url = item['url']
            if item_url:
                self.window.run_command("robot_framework_fetch_package", {"location": rfdocs_dir, "url": item_url})
