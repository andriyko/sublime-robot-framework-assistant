import unittest
import env
from os import path
from parser_utils.file_formatter import rf_table_name, lib_table_name
from get_documentation import GetKeywordDocumentation


class GetDocumentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_base = path.join(
            env.RESOURCES_DIR,
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

    def setUp(self):
        self.get_doc = GetKeywordDocumentation(
            table_dir=self.db_dir,
            index_dir=self.index_dir,
            open_tab=self.test_a_file)

    def test_kw_only(self):
        cell = 'No Operation'
        object_name = 'BuiltIn'
        doc = self.get_doc.return_documentation(object_name, cell)
        self.assertEqual(doc, 'Does absolutely nothing.')
        cell = 'Log'
        doc = self.get_doc.return_documentation(object_name, cell)
        expected = 'Logs the given message with'
        self.assertTrue(doc.startswith(expected))

    def test_error_conditions(self):
        cell = '${TEST_A}'
        object_name = None
        doc = self.get_doc.return_documentation(object_name, cell)
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
        table_name = self.get_doc.get_table_name_from_index(object_name, cell)
        self.assertEqual(self.builtin_table_name, table_name)
        cell = 'Test A Keyword'
        object_name = None
        table_name = self.get_doc.get_table_name_from_index(object_name, cell)
        self.assertEqual(self.test_a_table_name, table_name)
        object_name = ''
        table_name = self.get_doc.get_table_name_from_index(object_name, cell)
        self.assertEqual(self.test_a_table_name, table_name)

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

    @property
    def test_a_file(self):
        return path.normcase(path.join(self.suite_dir, 'test_a.robot'))

    @property
    def test_a_table_name(self):
        return rf_table_name(self.test_a_file)

    @property
    def builtin_table_name(self):
        return lib_table_name('BuiltIn')

    @property
    def test_a_index_name(self):
        return 'index-{0}'.format(self.test_a_table_name)

    @property
    def builtin_table_path(self):
        return path.join(self.db_dir, self.builtin_table_name)
