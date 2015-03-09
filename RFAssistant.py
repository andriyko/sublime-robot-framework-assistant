#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import os

try:
    from rfassistant import PY2
except ImportError:
    from .rfassistant import PY2

if PY2:
    from rfassistant import dynamic_data_file_path
    from rfassistant.rfdocs.commands.show_command import RobotFrameworkShowManifestCommand, \
        RobotFrameworkShowPackagesCommand
    from rfassistant.rfdocs.commands.validate_command import RobotFrameworkValidatePackagesCommand, \
        RobotFrameworkInsertIntoViewCommand
    from rfassistant.rfdocs.commands.download_command import \
        RobotFrameworkDownloadManifestCommand, RobotFrameworkFetchKeywordIntoViewCommand, \
        RobotFrameworkDownloadPackagesCommand, RobotFrameworkFetchManifestCommand, RobotFrameworkFetchPackageCommand
    from rfassistant.commands.scan_local_data_command import RobotFrameworkScanPythonLibsCommand, \
        RobotFrameworkScanResourceFilesCommand, \
        RobotFrameworkScanTestCaseFilesCommand, RobotFrameworkScanPythonLibsAndResourceFilesCommand
    from rfassistant.load_data import RFDataCollector, RobotFrameworkOpenItemDocCommand, \
        RobotFrameworkLogItemCommand, RobotFrameworkRecollectDataCommand, RobotFrameworkGoToItemSourceCommand, \
        RobotFrameworkScanCurrentFileCommand
    from rfassistant.syntax_highlight import AutoSyntaxHighlight
    from rfassistant.rflint.rflint_git import RobotFrameworkRflintGitStagedChangedFilesCommand, \
        RobotFrameworkRflintGitStagedChangedUntrackedFilesCommand
    from rfassistant.rflint.rflint_open_tab import RobotFrameworkRflintOpenTabCommand

else:
    from .rfassistant import dynamic_data_file_path
    from .rfassistant.rfdocs.commands.show_command import RobotFrameworkShowManifestCommand, RobotFrameworkShowPackagesCommand
    from .rfassistant.rfdocs.commands.validate_command import RobotFrameworkValidatePackagesCommand, RobotFrameworkInsertIntoViewCommand
    from .rfassistant.rfdocs.commands.download_command import \
        RobotFrameworkDownloadManifestCommand, RobotFrameworkFetchKeywordIntoViewCommand, \
        RobotFrameworkDownloadPackagesCommand, RobotFrameworkFetchManifestCommand, RobotFrameworkFetchPackageCommand
    from .rfassistant.commands.scan_local_data_command import RobotFrameworkScanPythonLibsCommand, \
        RobotFrameworkScanResourceFilesCommand, RobotFrameworkScanTestCaseFilesCommand, \
        RobotFrameworkScanPythonLibsAndResourceFilesCommand
    from .rfassistant.load_data import RFDataCollector, RobotFrameworkOpenItemDocCommand, \
        RobotFrameworkLogItemCommand, RobotFrameworkRecollectDataCommand, RobotFrameworkGoToItemSourceCommand, \
        RobotFrameworkScanCurrentFileCommand
    from .rfassistant.syntax_highlight import AutoSyntaxHighlight
    from .rfassistant.rflint.rflint_git import RobotFrameworkRflintGitStagedChangedFilesCommand, \
        RobotFrameworkRflintGitStagedChangedUntrackedFilesCommand
    from .rfassistant.rflint.rflint_open_tab import RobotFrameworkRflintOpenTabCommand


class RobotFrameworkAssistantInitializer(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        super(RobotFrameworkAssistantInitializer, self).__init__(*args, **kwargs)
        ### clean up current files data
        if os.path.exists(dynamic_data_file_path):
            os.unlink(dynamic_data_file_path)
