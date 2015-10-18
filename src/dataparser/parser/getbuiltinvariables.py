from robot.api import TestSuite
from os import path
from platform import system

ROOT_DIR = path.dirname(path.abspath(__file__))


class GetBuiltInVariables():

    def _run_rf(self):
        lib = path.join(ROOT_DIR, 'rf_get_vars.py')
        if system() is 'Windows':
            lib = lib.replace('\\', '\\\\')
        suite = TestSuite('Simple1')
        suite.resource.imports.library(lib)
        test = suite.tests.create('Test')
        test.keywords.create(name='get_internal_variables')
        suite.run(output='None', console='None')

    def get_builtin_vars(self):
        self._run_rf()
        from rf_vars import RF_VARS
        return RF_VARS
