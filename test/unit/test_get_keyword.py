import unittest
import env
import shutil
from os import path, mkdir
from index.index import Index
from queue.scanner import Scanner
from parser_utils.file_formatter import rf_table_name, lib_table_name
from get_keyword import GetKeyword


class TestGetKeyword(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_base = path.join(
            env.RESULTS_DIR,
            'database_in_package_dir')
        cls.db_dir = path.join(
            db_base,
            'db_dir'
        )
        cls.index_dir = path.join(
            db_base,
            'index_dir',
        )
        cls.suite_dir = path.join(
            env.TEST_DATA_DIR,
            'suite_tree'
        )
        if path.exists(db_base):
            shutil.rmtree(db_base)
        mkdir(db_base)
        mkdir(cls.db_dir)
        mkdir(cls.index_dir)
        scanner = Scanner()
        index = Index()
        scanner.scan(
            cls.suite_dir,
            'robot',
            cls.db_dir)
        index.index_all_tables(
            cls.db_dir,
            cls.index_dir)
        cls.rf_ext = 'robot'

    def setUp(self):
        self.get_kw = GetKeyword(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.get_common_robot_path,
            rf_extension=self.rf_ext
        )

    def test_return_file_and_patter(self):
        kw = 'Common Keyword 2'
        object_name = None
        expected_path = path.normcase(self.get_common_robot_path)
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)
        object_name = 'common'
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)
        kw = 'common keyword 2'
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)
        kw = 'COMMON KEYWORD 2'
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)
        kw = 'Common_Keyword_2'
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)
        kw = 'CommonKeyword2'
        regex, file_path = self.get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        self.assertEqual(file_path, expected_path)

    def test_with_test_a_robot(self):
        get_kw = GetKeyword(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_a_file,
            rf_extension=self.rf_ext
        )
        kw = 'Resource A Keyword 1'
        object_name = None
        regex, file_path = get_kw.return_file_and_patter(object_name, kw)
        self.assertEqual(regex, '(?im)^resource[_ ]?a[_ ]?keyword[_ ]?1$')
        self.assertEqual(file_path, self.resource_a_table_file)

    def test_get_regex_resource(self):
        kw = 'Common Keyword 2'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        kw = 'RUN'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, '(?im)^run$')
        kw = 'Common_Keyword_2'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        kw = 'CommonKeyword2'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        kw = 'commonKeyword2'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)
        kw = 'COMMON KEYWORD 2'
        regex = self.get_kw.get_regex_resource(kw)
        self.assertEqual(regex, self.get_common_keyword_2_regex)

    def test_rf_data(self):
        self.assertTrue(self.get_kw.rf_data(self.get_common_robot_path))
        self.assertFalse(self.get_kw.rf_data(self.get_common_variables_path))

    @property
    def get_common_robot(self):
        return 'common.robot'

    @property
    def get_common_robot_path(self):
        return path.join(self.suite_dir, self.get_common_robot)

    @property
    def get_common_keyword_2_regex(self):
        return '(?im)^common[_ ]?keyword[_ ]?2$'

    @property
    def get_common_variables_path(self):
        return path.join(self.suite_dir, 'common_variables.py')

    @property
    def test_a_file(self):
        return path.normcase(path.join(self.suite_dir, 'test_a.robot'))

    @property
    def resource_a_table_file(self):
        return path.normcase(path.join(self.suite_dir, 'resource_a.robot'))

    @property
    def test_a_table_name(self):
        return rf_table_name(self.test_a_file)

    @property
    def resource_a_table_name(self):
        return rf_table_name(self.resource_a_table_file)
