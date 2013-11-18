#!/usr/bin/env python

import sublime
import sublime_plugin

try:
    from rfassistant import settings_filename, libs_manifest_path, libs_dir_path, libs_update_url_default
    from rfassistant.commands.show_command import RobotFrameworkShowManifestCommand, RobotFrameworkShowPackagesCommand
    from rfassistant.commands.validate_command import RobotFrameworkValidatePackagesCommand, RobotFrameworkInsertIntoViewCommand
    from rfassistant.commands.download_command import \
        RobotFrameworkDownloadManifestCommand, RobotFrameworkFetchKeywordIntoViewCommand, \
        RobotFrameworkDownloadPackagesCommand, RobotFrameworkFetchManifestCommand, RobotFrameworkFetchPackageCommand
    from rfassistant.load_keywords import RFKeywordCollector, RobotFrameworkOpenKeywordDocCommand, \
        RobotFrameworkFetchKeywordDocCommand, RobotFrameworkReindexPackagesCommand
    from rfassistant.syntax_highlight import AutoSyntaxHighlight
except ImportError:
    from .rfassistant import settings_filename, libs_manifest_path, libs_dir_path, libs_update_url_default
    from .rfassistant.commands.show_command import RobotFrameworkShowManifestCommand, RobotFrameworkShowPackagesCommand
    from .rfassistant.commands.validate_command import RobotFrameworkValidatePackagesCommand,RobotFrameworkInsertIntoViewCommand
    from .rfassistant.commands.download_command import \
        RobotFrameworkDownloadManifestCommand, RobotFrameworkDownloadPackagesCommand, \
        RobotFrameworkFetchManifestCommand, RobotFrameworkFetchPackageCommand, RobotFrameworkFetchKeywordIntoViewCommand
    from .rfassistant.load_keywords import RFKeywordCollector, RobotFrameworkOpenKeywordDocCommand, \
        RobotFrameworkFetchKeywordDocCommand, RobotFrameworkReindexPackagesCommand
    from .rfassistant.syntax_highlight import AutoSyntaxHighlight


class RobotFrameworkAssistantInitializer(sublime_plugin.WindowCommand):
    s = None
    libs_update_url_placeholder = libs_update_url_default
    libs_manifest_placeholder = libs_manifest_path
    libs_dir_placeholder = libs_dir_path
    # need silly options below because autocomplete box is too narrow to show options normally
    # Please see Sublime Text2 ticket
    # http://sublimetext.userecho.com/topic/85632-need-the-completion-menu-to-be-wider/
    show_version_in_autocomplete_box = True
    show_library_before_version = True

    def __init__(self, *args, **kwargs):
        super(RobotFrameworkAssistantInitializer, self).__init__(*args, **kwargs)
        s = sublime.load_settings(settings_filename)
        for prop, value in (['libs_update_url', self.libs_update_url_placeholder],
                            ['libs_manifest', self.libs_manifest_placeholder],
                            ['show_version_in_autocomplete_box', self.show_version_in_autocomplete_box],
                            ['show_library_before_version', self.show_library_before_version],
                            ['libs_dir', self.libs_dir_placeholder]):
            if not s.has(prop):
                s.set(prop, value)
        sublime.save_settings(settings_filename)


def plugin_loaded():
    #TODO add some validation?
    pass