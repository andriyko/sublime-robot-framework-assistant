import unittest
import env
from os import path
from return_keyword_table import ReturnKeywordAndObject


class TestCompletions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.current_view = path.join(env.RESOURCES_DIR, 'current_view.json')
        cls.rf_cell = '    '
        cls.rkao = ReturnKeywordAndObject(cls.current_view, cls.rf_cell)

    def test_get_rf_cell(self):
        kw_in_line = 'Comment'
        line = '{0}{1}'.format(self.rf_cell, kw_in_line)
        # column at end of line
        column = len(line)
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, kw_in_line)
        # column at middle of keyword
        column = 5
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, kw_in_line)
        # column at start of keyword
        column = 4
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, kw_in_line)
        # column off from keyword
        column = 2
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, None)
        # Multiple keyword in line, column in middle
        kw_1_in_line = 'Run Keyword'
        kw_2_in_line = 'Log'
        argument = 'Some Text'
        column = 20
        line = '{0}{1}{0}{2}{0}{3}'.format(
            self.rf_cell,
            kw_1_in_line,
            kw_2_in_line,
            argument
        )
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, kw_2_in_line)
        # Multiple keyword in line, column in middle of space in kw
        column = 7
        rf_cell = self.rkao.get_rf_cell(line, column)
        self.assertEqual(rf_cell, kw_1_in_line)

    def test_get_data(self):
        self.rkao._get_data()
        self.assertTrue('completion' in self.rkao.data)
