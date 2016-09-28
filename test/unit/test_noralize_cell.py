import unittest
import env
import json
from os import path
from noralize_cell import ReturnKeywordAndObject


class TestCompletions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.current_view = path.join(
            env.RESOURCES_DIR,
            'index-test_a.robot-c6b0faa0427a2cf861a1acad630765ea.json'
        )
        cls.rf_cell = '    '
        cls.rkao = ReturnKeywordAndObject(
            cls.current_view,
            cls.rf_cell
        )

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

    def test_normalize_kw_only(self):
        kw = 'Comment'
        line = '{0}{1}'.format(self.rf_cell, kw)
        column = len(line)
        keyword, object_name = self.rkao.normalize(line, column)
        self.assertEqual(keyword, kw)
        self.assertEqual(object_name, None)

    def test_normalize_kw_and_lib(self):
        kw = 'Comment'
        library = 'BuiltIn'
        line = '{0}{1}.{2}'.format(self.rf_cell, library, kw)
        column = len(line) - 1
        keyword, object_name = self.rkao.normalize(line, column)
        self.assertEqual(object_name, library)
        self.assertEqual(keyword, kw)
        kw = 'Common Keyword 2'
        library = 'common'
        line = '{0}{1}.{2}'.format(self.rf_cell, library, kw)
        column = len(line) - 1
        keyword, object_name = self.rkao.normalize(line, column)
        self.assertEqual(keyword, kw)
        self.assertEqual(object_name, library)

    def test_normalize_long_lib_and_space_in_kw(self):
        kw = 'My Long Keyword'
        library = 'com.company.library.DoLibrary'
        line = '{0}{1}.{2}'.format(self.rf_cell, library, kw)
        column = len(line) - 6
        keyword, object_name = self.rkao.normalize(line, column)
        self.assertEqual(object_name, library)
        self.assertEqual(keyword, kw)

    def test_separate_keyword_from_object_no_space(self):
        kw = 'Comment'
        library = 'BuiltIn'
        cell = '{0}.{1}'.format(library, kw)
        object_name, keyword = self.rkao.separate_keyword_from_object(cell)
        self.assertEqual(object_name, library)
        self.assertEqual(keyword, kw)

    def test_separate_keyword_from_object_space(self):
        kw = 'Import Library'
        library = 'BuiltIn'
        cell = '{0}.{1}'.format(library, kw)
        object_name, keyword = self.rkao.separate_keyword_from_object(cell)
        self.assertEqual(object_name, library)
        self.assertEqual(keyword, kw)

    def test_separate_keyword_from_object_lib_with_dots(self):
        kw = 'My Long Keyword'
        library = 'com.company.library.DoLibrary'
        cell = '{0}.{1}'.format(library, kw)
        object_name, keyword = self.rkao.separate_keyword_from_object(cell)
        self.assertEqual(object_name, library)
        self.assertEqual(keyword, kw)

    def test_get_data(self):
        self.rkao._get_data()
        self.assertTrue('keywords' in self.rkao.data)
        self.assertGreater(len(self.rkao.data['keywords']), 1)

    def test_library_too_long_name(self):
        current_view_ = path.join(
            env.RESOURCES_DIR,
            'index-test_b.robot-28dc4d6e222a03bbc3db1fe62743ce94.json'
        )
        rkao_ = ReturnKeywordAndObject(
            current_view_,
            '    '
        )
        line = (
            '    OtherNameLib.Keyword Which Also Has Really Long Name But '
            'Not As Long The Class Name By 1234 In Keyword'
        )
        column = 30
        keyword, object_name = rkao_.normalize(line, column)
        self.assertEqual(keyword, line.replace('    OtherNameLib.', ''))
        self.assertEqual(object_name, 'OtherNameLib')

    @property
    def add_dolibrary_kw1(self):
        return [
            "My Long Keyword", [
                "arg1",
                "arg2"
            ],
            "com.company.library.DoLibrary"
        ]

    @property
    def add_dolibrary_kw2(self):
        return [
            "My Other Keyword", [
                "arg1",
                "arg2",
                "arg3"
            ],
            "com.company.library.DoLibrary"
        ]

    @property
    def add_otherlibrary_kw1(self):
        return [
            "My Long Keyword", [
                "arg1",
                "arg2"
            ],
            "com.company.library.OtherLibrary"
        ]

    @property
    def add_spical_long_otherlibrary_kw1(self):
        return [
            "My Long Keyword", [
                "arg1",
                "arg2"
            ],
            "com.company.library.special.long.OtherLibrary"
        ]

    def do_setup(self):
        f = open(self.current_view)
        data = json.load(f)
        f.close()
        completion = data['completion']
        completion.append(self.add_dolibrary_kw1)
        completion.append(self.add_dolibrary_kw2)
        completion.append(self.add_otherlibrary_kw1)
        completion.append(self.add_spical_long_otherlibrary_kw1)
        data['completion'] = completion
        f = open(self.current_view, 'w')
        json.dump(data, f, indent=4)
        f.close()
        self.do_setup = True
