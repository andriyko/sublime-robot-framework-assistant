import unittest
import env
import os
import shutil
from time import sleep
from queue.scanner import Scanner
from workspace_objects import WorkSpaceObjects


class TestWorspaceObjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        scanner = Scanner()
        cls.db_dir = os.path.join(
            env.RESULTS_DIR,
            'scanner',
            'db_dir'
        )
        cls.real_suite = os.path.join(
            env.TEST_DATA_DIR,
            'real_suite')
        if os.path.exists(cls.db_dir):
            while os.path.exists(cls.db_dir):
                shutil.rmtree(cls.db_dir)
                sleep(0.1)
            os.mkdir(cls.db_dir)
        scanner.scan(
            cls.real_suite,
            'robot',
            cls.db_dir)
        cls.objects = WorkSpaceObjects(cls.db_dir)

    def test_get_libaries(self):
        libs = self.objects.get_libraries()
        self.assertEqual(len(libs), 3)
        self.assertFalse(['BuiltIn', 'BuiltIn'] in libs)
        self.assertTrue(['Selenium2Library', 'Selenium2Library'] in libs)

    def test_get_resources(self):
        res = self.objects.get_resources()
        self.assertEqual(len(res), 3)
        res_item = res[0]
        self.assertTrue(res_item[0].endswith('.robot'))
        self.assertTrue(res_item[1].endswith('.robot'))

    def test_get_variables(self):
        vars_ = self.objects.get_variables()
        self.assertEqual(len(vars_), 1)
        self.assertTrue(vars_[0][0].endswith('variables.py'))
        self.assertTrue(vars_[0][1].endswith('variables.py'))

    def test_get_imports(self):
        imports = self.objects.get_imports('library')
        self.assertEqual(len(imports), 3)
        imports = self.objects.get_imports('variable_file')
        self.assertEqual(len(imports), 1)
        imports = self.objects.get_imports('resource_file')
        self.assertEqual(len(imports), 3)
