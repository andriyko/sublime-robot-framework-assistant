#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python imports
import os
import subprocess


class BinaryNotFoundError(Exception):
    pass


class NonCleanExitError(Exception):
    def __init__(self, returncode):
        self.returncode = returncode

    def __str__(self):
        return repr(self.returncode)


class CliDownloader():
    def find_binary(self, name):
        for d in os.environ['PATH'].split(os.pathsep):
            path = os.path.join(d, name)
            if os.path.exists(path):
                return path
        raise BinaryNotFoundError('The binary {0} could not be located'.format(name))

    def execute(self, args):
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output = proc.stdout.read()
        returncode = proc.wait()
        if returncode != 0:
            error = NonCleanExitError(returncode)
            error.output = output
            raise error
        return output
