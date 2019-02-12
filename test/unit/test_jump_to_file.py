import os
import shutil
import unittest

from index_runner import index_all
from jump_to_file import JumpToFile
from queue.scanner import Scanner
import env


class TestJumpToFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_base = os.path.join(
            env.RESULTS_DIR,
            'database_jump_to_file')
        cls.db_dir = os.path.join(
            db_base,
            'db_dir'
        )
        cls.index_dir = os.path.join(
            db_base,
            'index_dir',
        )
        cls.suite_dir = os.path.join(
            env.TEST_DATA_DIR,
            'suite_tree'
        )
        if os.path.exists(db_base):
            shutil.rmtree(db_base)
        os.mkdir(db_base)
        os.mkdir(cls.db_dir)
        os.mkdir(cls.index_dir)
        scanner = Scanner()
        scanner.scan(
            cls.suite_dir,
            'robot',
            cls.db_dir)
        index_all(cls.db_dir, cls.index_dir)
        cls.rf_ext = 'robot'

    def setUp(self):
        self.jump = JumpToFile()

    def test_is_resource(self):
        line = 'Resource          common.robot'
        status = self.jump.is_import(line)
        self.assertTrue(status)

        line = '| Resource      | common.robot |'
        status = self.jump.is_import(line)
        self.assertTrue(status)

        line = '| Resource | common.robot |'
        status = self.jump.is_import(line)
        self.assertTrue(status)

    def test_is_library(self):
        line = 'Library          Selenium2Library'
        status = self.jump.is_import(line)
        self.assertTrue(status)

        line = '| Library      | Selenium2Library |'
        status = self.jump.is_import(line)
        self.assertTrue(status)

        line = '| Library | Selenium2Library |'
        status = self.jump.is_import(line)
        self.assertTrue(status)

    def test_get_import_with_resource_space_separator(self):
        line = 'Resource          ../bar/foo/foonar/common.robot'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, '../bar/foo/foonar/common.robot')

    def test_get_import_with_resource_space_pipe(self):
        line = '| Resource      | common.robot |'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, 'common.robot')

        line = '| Resource | common.robot |'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, 'common.robot')

    def test_get_import_with_library_space_separator(self):
        line = 'Library          common.robot'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, 'common.robot')

    def test_get_import_with_library_space_pipe(self):
        line = '| Library      | common |'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, 'common')

        line = '| Library | foo/bar/common.py |'
        imported = self.jump.get_import(line)
        self.assertEqual(imported, 'foo/bar/common.py')

    def test_get_import_resource_path(self):
        if os.sep == '/':
            open_tab = '/workspace/resource/file.robot'
        else:
            open_tab = 'C:\\workspace\\resource\\file.robot'
        path = self.jump.get_path_resource_path(
            imported_file='Foo/Bar/CommonFile.robot',
            open_tab=open_tab
        )
        if os.sep == '/':
            expected = (
                '/workspace/resource/'
                'Foo/Bar/CommonFile.robot'
            )
        else:
            expected = (
                'C:\\workspace\\resource\\'
                'Foo\\Bar\\CommonFile.robot'
            )
        self.assertEqual(path, expected)

    def test_get_import_lib_with_path(self):
        if os.sep == '/':
            open_tab = '/workspace/resource/file.robot'
        else:
            open_tab = 'C:\\workspace\\resource\\file.robot'
        path = self.jump.get_library_path(
            imported_lib='Foo/Bar/CommonLib.py',
            open_tab=open_tab,
            db_dir=self.db_dir
        )
        if os.sep == '/':
            expected = (
                '/workspace/resource/'
                'Foo/Bar/CommonLib.py'
            )
        else:
            expected = (
                'C:\\workspace\\resource\\'
                'Foo\\Bar\\CommonLib.py'
            )
        self.assertEqual(path, expected)

    def test_get_import_lib_with_object_name(self):
        if os.sep == '/':
            open_tab = '/workspace/resource/file.robot'
        else:
            open_tab = 'C:\\workspace\\resource\\file.robot'
        path = self.jump.get_library_path(
            imported_lib='BuiltIn',
            open_tab=open_tab,
            db_dir=self.db_dir
        )
        self.assertTrue(os.path.isfile(path))

    def test_get_path_with_lib(self):
        if os.sep == '/':
            open_tab = '/workspace/resource/file.robot'
        else:
            open_tab = 'C:\\workspace\\resource\\file.robot'
        path = self.jump.get_import_path(
            import_='BuiltIn',
            open_tab=open_tab,
            db_dir=self.db_dir
        )
        self.assertTrue(os.path.isfile(path))

    def test_get_path_with_resouce(self):
        if os.sep == '/':
            open_tab = '/workspace/resource/file.robot'
        else:
            open_tab = 'C:\\workspace\\resource\\file.robot'
        path = self.jump.get_import_path(
            import_='Foo/Bar/CommonLib.robot',
            open_tab=open_tab,
            db_dir=self.db_dir
        )
        self.assertTrue(path)
