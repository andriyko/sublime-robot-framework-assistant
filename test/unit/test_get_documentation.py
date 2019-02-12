import unittest
import env
import shutil
from os import path, makedirs
from index_runner import index_all
from queue.scanner import Scanner
from parser_utils.file_formatter import rf_table_name, lib_table_name
from get_documentation import GetKeywordDocumentation


class GetDocumentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rf_extension = 'robot'
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
        makedirs(cls.db_dir)
        makedirs(cls.index_dir)
        scanner = Scanner()
        scanner.scan(
            cls.suite_dir,
            cls.rf_extension,
            cls.db_dir)
        index_all(cls.db_dir, cls.index_dir)

    def setUp(self):
        self.get_doc = GetKeywordDocumentation(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_a_file
        )

    def test_kw_only(self):
        cell = 'No Operation'
        object_name = 'BuiltIn'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, 'Does absolutely nothing.')
        cell = 'Log'
        doc = self.get_doc.return_documentation(object_name, cell)
        expected = 'Logs the given message with'
        self.assertTrue(doc.startswith(expected))

    def test_user_kw_with_module(self):
        object_name = 'test_a'
        cell = 'Test A Keyword'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, 'Some Doc Here')

    def test_error_conditions(self):
        cell = '${TEST_A}'
        object_name = None
        doc = self.get_doc.return_documentation(
            object_name, cell)
        self.assertEqual(doc, None)
        object_name = ''
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)
        cell = 'Not Here'
        object_name = 'BuiltIn'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)
        cell = 'No Operation'
        object_name = 'NotBuiltInModule'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)

    def test_module_name_not_correct(self):
        cell = 'No Operation'
        object_name = '_BuiltIn'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)
        object_name = 'builtin'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)
        object_name = 'BUILTIN'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, None)

    def test_get_table_name_from_index(self):
        cell = 'No Operation'
        object_name = 'BuiltIn'
        kw_details = self.get_doc.get_table_name_from_index(
            object_name, cell)
        self.assertEqual(kw_details.table_name, self.builtin_table_name)
        self.assertEqual(kw_details.kw, cell)
        self.assertEqual(kw_details.kw_object_name, object_name)
        cell = 'Test A Keyword'
        object_name = None
        kw_details = self.get_doc.get_table_name_from_index(
            object_name, cell)
        self.assertEqual(kw_details.table_name, self.test_a_table_name)
        self.assertEqual(kw_details.kw, cell)
        self.assertEqual(kw_details.kw_object_name, 'test_a')
        object_name = ''
        kw_details = self.get_doc.get_table_name_from_index(
            object_name,
            cell
        )
        self.assertEqual(kw_details.table_name, self.test_a_table_name)
        self.assertEqual(kw_details.kw, cell)
        self.assertEqual(kw_details.kw_object_name, 'test_a')
        object_name = 'test_a'
        kw_details = self.get_doc.get_table_name_from_index(
            object_name, cell)
        self.assertEqual(kw_details.table_name, self.test_a_table_name)
        self.assertEqual(kw_details.kw, cell)
        self.assertEqual(kw_details.kw_object_name, object_name)
        cell = 'Resource A Keyword 1'
        object_name = None
        kw_details = self.get_doc.get_table_name_from_index(
            object_name, cell)
        self.assertEqual(kw_details.table_name, self.resource_a_table_name)
        self.assertEqual(kw_details.kw, cell)
        self.assertEqual(kw_details.kw_object_name, 'resource_a')

    def test_get_table_name_from_index_with_test_b(self):
        _get_doc = GetKeywordDocumentation(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_b_file
        )
        cell = (
            'Keyword Which Also Has Really Long Name But '
            'Not As Long The Class Name By 1234 In Keyword'
        )
        object_name = 'OtherNameLib'
        kw_details = _get_doc.get_table_name_from_index(
            object_name, cell
        )
        self.assertEqual(kw_details.table_name, self.othernamelib_table_name)
        self.assertEqual(kw_details.kw, cell.replace('1234', '${argument}'))
        self.assertEqual(
            kw_details.kw_object_name,
            (
                'LibraryNameWhichIsLongerThan100CharactersButItSeemsThatIt'
                'RequiresQuiteAlotLettersInTheFileName'
                'AndIsNotGoodRealLifeExample'
            )
        )

    def test_get_keyword_documentation(self):
        cell = 'No Operation'
        object_name = 'BuiltIn'
        expected_doc = 'Does absolutely nothing.'
        doc = self.get_doc.get_keyword_documentation(
            self.builtin_table_path,
            object_name,
            cell)
        self.assertEqual(doc, expected_doc)
        cell = 'Log'
        expected_doc = 'Logs the given message with'
        doc = self.get_doc.get_keyword_documentation(
            self.builtin_table_path,
            object_name,
            cell)
        self.assertTrue(doc.startswith(expected_doc))

    def test_embedding_arg_kw_doc(self):
        _get_doc = GetKeywordDocumentation(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_b_file
        )
        doc = _get_doc.return_documentation(
            '',
            'Embedding arg To Keyword Name'
        )
        self.assertEqual(doc, 'Keyword with embedding arg to keyword name')

        kw = (
            'Keyword Which Also Has Really Long Name But Not As'
            ' Long The Class Name By 1234 In Keyword'
        )
        doc = _get_doc.return_documentation(
            'OtherNameLib',
            kw
        )
        self.assertEqual(doc, 'Documentation is here')

    def test_get_table_name_from_index_with_embedding_arg_kw(self):
        _get_doc = GetKeywordDocumentation(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_b_file
        )
        kw_details = _get_doc.get_table_name_from_index(
            '',
            'Embedding arg To Keyword Name'
        )
        self.assertEqual(kw_details.table_name, self.resource_b_table_name)
        self.assertEqual(kw_details.kw, 'Embedding ${arg} To Keyword Name')
        self.assertEqual(kw_details.kw_object_name, 'resource_b')

    @property
    def test_a_file(self):
        return path.normcase(path.join(self.suite_dir, 'test_a.robot'))

    @property
    def test_b_file(self):
        return path.normcase(path.join(self.suite_dir, 'test_b.robot'))

    @property
    def resource_a_table_file(self):
        return path.normcase(path.join(self.suite_dir, 'resource_a.robot'))

    @property
    def resource_b_table_file(self):
        return path.normcase(path.join(self.suite_dir, 'resource_b.robot'))

    @property
    def test_a_table_name(self):
        return rf_table_name(self.test_a_file)

    @property
    def resource_a_table_name(self):
        return rf_table_name(self.resource_a_table_file)

    @property
    def resource_b_table_name(self):
        return rf_table_name(self.resource_b_table_file)

    @property
    def builtin_table_name(self):
        return lib_table_name('BuiltIn')

    @property
    def test_a_index_name(self):
        return 'index-{0}'.format(self.test_a_table_name)

    @property
    def builtin_table_path(self):
        return path.join(self.db_dir, self.builtin_table_name)

    @property
    def othernamelib_table_name(self):
        return lib_table_name(
            'LibraryNameWhichIsLongerThan100CharactersButItSeemsThatItRequires'
            'QuiteAlotLettersInTheFileNameAndIsNotGoodRealLifeExample'
        )
