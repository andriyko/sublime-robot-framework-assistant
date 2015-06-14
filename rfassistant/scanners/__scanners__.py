#!/usr/bin/env python
# -*- coding: utf-8 -*-

# No sublime imports here.
# This module should be used with system python interpreter
# (outside of Sublime's python interpreter).

import os
import sys

from rfassistant.scanners_wrapper import get_modules, ScannersWrapper

modules_str = get_modules(os.path.dirname(os.path.realpath(__file__)))
modules_objects = [
    __import__(module, globals=globals(), locals=locals(), fromlist="*") for module in modules_str
]
sys.modules[__name__] = ScannersWrapper(modules_objects)
