import unittest
import env
import shutil
import platform
from os import path, mkdir
from index_runner import index_all
from queue.scanner import Scanner
from get_keyword import GetKeyword


class TestGetKeywordFromLibrary(unittest.TestCase):

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
        scanner.scan(
            cls.suite_dir,
            'robot',
            cls.db_dir)
        index_all(cls.db_dir, cls.index_dir)
        cls.rf_ext = 'robot'

    def setUp(self):
        self.get_kw = GetKeyword(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.get_common_robot_path,
            rf_extension=self.rf_ext
        )

    def test_get_lib_kw(self):
        regex, file_path = self.get_kw.get_lib_keyword(
            self.s2l_table_file,
            None,
            'Simulate'
        )
        self.assertIsNotNone(regex)
        self.assertIsNotNone(file_path)

    def test_get_lib_keyword_file(self):
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            None,
            'Simulate'
        )
        self.assertIn(self.s2l_simulate, kw_file)
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            None,
            'textarea_value_should_be'
        )
        self.assertIn(self.s2l_textarea_value_should_be, kw_file)
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            None,
            'PressKey'
        )
        self.assertIn(self.s2l_press_key, kw_file)
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            'Selenium2Library',
            'PressKey'
        )
        self.assertIn(self.s2l_press_key, kw_file)
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            'NotHere',
            'PressKey'
        )
        self.assertEqual(kw_file, None)
        kw_file = self.get_kw.get_lib_keyword_file(
            self.s2l_table_file,
            None,
            'NotKeyword'
        )
        self.assertEqual(kw_file, None)

    def test_get_regex_library(self):
        kw = 'Simulate'
        regex = self.get_kw.get_regex_library(kw)
        self.assertEqual(
            regex,
            r'(?im)(def simulate\()|(\@keyword.+name=[\'"]simulate)'
        )
        kw = 'Press Key'
        regex = self.get_kw.get_regex_library(kw)
        self.assertEqual(
            regex,
            r'(?im)(def press_?key\()|(\@keyword.+name=[\'"]press[_ ]key)'
        )
        kw = 'Embedding ${arg} To Keyword Name'
        regex = self.get_kw.get_regex_library(kw)
        self.assertEqual(
            regex,
            (
                r'(?i)(\@keyword.+name=[\'"]'
                r'embedding[_ ]?\$\{.+\}[_ ]?to[_ ]?keyword[_ ]?name)'
            )
        )
        regex = self.get_kw.get_regex_library('Other ${arg1} and ${arg2} Too')
        self.assertEqual(
            regex,
            (
                r'(?i)(\@keyword.+name=[\'"]'
                r'other[_ ]?\$\{.+\}[_ ]?and[_ ]?\$\{.+\}[_ ]?too)'
            )
        )

    def test_keyword_lib_with_alias(self):
        get_kw_ = GetKeyword(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.get_resource_b_robot_path,
            rf_extension=self.rf_ext
        )
        # regex, file_path = get_kw_.return_file_and_patter(
        #     'LongName',
        #     'Long Name Keyword'
        # )
        # self.assertEqual(
        #     file_path,
        #     self.long_name_file
        # )

        kw = (
            'Keyword Which Also Has Really Long Name But Not As'
            ' Long The Class Name By 1234 In Keyword'
        )
        regex, file_path = get_kw_.return_file_and_patter(
            'OtherNameLib',
            kw
        )
        expected_re = (
            '(?i)(\\@keyword.+name=[\\\'"]'
            'keyword[_ ]?which[_ ]?also[_ ]?has[_ ]?really'
            '[_ ]?long[_ ]?name[_ ]?but[_ ]?not[_ ]?as'
            '[_ ]?long[_ ]?the[_ ]?class[_ ]?name[_ ]?by'
            '[_ ]?\\$\\{.+\\}[_ ]?in[_ ]?keyword)'
        )
        self.assertEqual(
            file_path,
            self.get_resource_lib_longer_than_100_chars
        )
        self.assertEqual(regex, expected_re)

    @property
    def s2l(self):
        if platform.system() == 'Windows':
            return 'selenium2library'
        else:
            return 'Selenium2Library'

    @property
    def s2l_simulate(self):
        return path.join(self.s2l, 'keywords', '_element.py')

    @property
    def s2l_press_key(self):
        return path.join(self.s2l, 'keywords', '_element.py')

    @property
    def s2l_textarea_value_should_be(self):
        return path.join(self.s2l, 'keywords', '_formelement.py')

    @property
    def s2l_table_file(self):
        return path.join(
            self.db_dir,
            'Selenium2Library-ac72a5ed5dae4edc06e58114b7c0ce92.json'
        )

    @property
    def get_common_robot(self):
        return 'common.robot'

    @property
    def get_common_robot_path(self):
        return path.join(self.suite_dir, self.get_common_robot)

    @property
    def long_name_file(self):
        return path.join(
            path.normcase(self.suite_dir), 'LibraryWithReallyTooLongName.py'
        )

    @property
    def get_resource_b_robot_path(self):
        return path.join(self.suite_dir, 'resource_b.robot')

    @property
    def get_resource_lib_longer_than_100_chars(self):
        return path.join(
            path.normcase(self.suite_dir),
            (
                'LibraryNameWhichIsLongerThan100CharactersButItSeemsThatIt'
                'RequiresQuiteAlotLettersInTheFileNameAndIsNotGoodReal'
                'LifeExample.py'
            )
        )
