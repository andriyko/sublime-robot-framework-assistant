#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter
# (outside of Sublime's python interpreter).

from .base import PythonLibParserBase, ResourceFileParserBase, TestCaseFileParserBase


class PythonLibParserStandard(PythonLibParserBase):
    pass


class ResourceFileParserStandard(ResourceFileParserBase):
    pass


class TestCaseFileParserStandard(TestCaseFileParserBase):
    pass
