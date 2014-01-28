#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter (outside of Sublime's python interpreter).

from ..scanners.base import PythonLibsScannerBase, ResourceFilesScannerBase, TestCaseFilesScannerBase

is_scanner = True


class PythonLibsScannerStandard(PythonLibsScannerBase):
    pass


class ResourceFilesScannerStandard(ResourceFilesScannerBase):
    pass


class TestCaseFilesScannerStandard(TestCaseFilesScannerBase):
    pass
