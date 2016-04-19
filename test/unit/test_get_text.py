import unittest
from utils.get_text import get_object_from_line


class TestCompletions(unittest.TestCase):

    def test_no_object(self):
        line = '    run'
        prefix = line.strip(' ')
        column = len(line)
        expected = get_object_from_line(line, prefix, column)
        self.assertEqual(expected, None)

    def test_object(self):
        line = '    BuiltIn.run'
        prefix = 'run'
        column = len(line)
        expected = get_object_from_line(line, prefix, column)
        self.assertEqual(expected, 'BuiltIn')

    def test_two_object_cursor_at_end(self):
        line = '{0}Run Keyword And Expect Error{1}no'.format(
            '    BuiltIn.', '    Selenium2Library.')
        prefix = 'no'
        column = len(line)
        expected = get_object_from_line(line, prefix, column)
        self.assertEqual(expected, 'Selenium2Library')

    def test_two_object_cursor_at_first(self):
        line = '{1}no{0}Run Keyword And Expect Error'.format(
            '    BuiltIn.', '    Selenium2Library.')
        prefix = 'no'
        column = 23
        expected = get_object_from_line(line, prefix, column)
        self.assertEqual(expected, 'Selenium2Library')
