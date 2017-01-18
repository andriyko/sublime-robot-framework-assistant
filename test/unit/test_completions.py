import unittest
import env
from os import path
from completions import get_kw_re_string
from completions import get_kw_completion_list
from completions import create_kw_completion_item
from completions import create_var_completion_item
from completions import get_var_completion_list
from completions import get_var_re_string
from completions import get_completion_list
from completions import get_var_mode
from completions import check_prefix
from completions import add_with_name

RF_CELL = '    '
RF_EXTENSION = 'robot'


class TestCompletions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_a_index = path.join(
            env.RESOURCES_DIR,
            'index-test_a.robot-c6b0faa0427a2cf861a1acad630765ea.json'
        )
        cls.test_b_index = path.join(
            env.RESOURCES_DIR,
            'index-test_b.robot-28dc4d6e222a03bbc3db1fe62743ce94.json'
        )

    def test_get_completion_list(self):
        prefix = 'Runk'
        result = get_completion_list(
            self.test_a_index, prefix, len(prefix), None, False, RF_CELL)
        self.assertEqual(len(result), 20)
        result = get_completion_list(
            self.test_a_index, '$', 1, None, False, RF_CELL)
        self.assertEqual(len(result), 30)
        result = get_completion_list(
            self.test_a_index, '${}', 2, None, False, RF_CELL)
        self.assertEqual(len(result), 30)

    def test_object_name_included(self):
        prefix = 'uilt'
        result = get_completion_list(
            self.test_a_index,
            prefix,
            4,
            '',
            False,
            RF_CELL
        )
        self.assertEqual(len(result), 23)
        builtin = 'BuiltIn'
        expected = (
            '{0}\t{0}'.format(builtin),
            '{0}.'.format(builtin,)
        )
        self.assertEqual(result[0], expected)

    def test_get_kw_re_string(self):
        re_string = get_kw_re_string('1')
        self.assertEqual(re_string, '(?i)(.*1)')
        re_string = get_kw_re_string('123')
        self.assertEqual(re_string, '(?i)(.*1.*2.*3)')
        re_string = get_kw_re_string(123)
        self.assertEqual(re_string, '(?i)(.*1.*2.*3)')

    def test_get_kw_completion_list_count(self):
        prefix = 'Run'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, None, False)
        self.assertEqual(len(kw_tuple), 40)
        prefix = 'RunKeY'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, None, False)
        self.assertEqual(len(kw_tuple), 20)
        prefix = 'BUI'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, None, False)
        self.assertEqual(len(kw_tuple), 13)

    def test_get_kw_completion_list_structure(self):
        prefix = 'Run'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, None, False)
        kw = 'Run Keyword And Expect Error'
        expected = (
            '{0}\tBuiltIn'.format(kw),
            '{0}{1}expected_error{1}name{1}*args'.format(kw, '\n...' + RF_CELL)
        )
        self.assertEqual(kw_tuple[0], expected)
        kw = 'Run And Return Rc'
        expected = (
            '{0}\tOperatingSystem'.format(kw),
            '{0}{1}command'.format(kw, '\n...' + RF_CELL))
        self.assertEqual(kw_tuple[-1], expected)
        kw_tuple = get_kw_completion_list(self.test_b_index, 'Embedding',
                                          RF_CELL, None, False)
        expected = (
            'Embedding ${arg} To Keyword Name\tresource_b',
            'Embedding \\${arg} To Keyword Name'
        )
        self.assertEqual(kw_tuple[0], expected)
        kw_tuple = get_kw_completion_list(self.test_b_index, 'Embedding',
                                          RF_CELL, None, True)
        self.assertEqual(kw_tuple[0], expected)
        self.assertEqual(len(kw_tuple), 1)

    def test_get_kw_completion_list_structure_with_object(self):
        object_name = 'test_a'
        prefix = 'test'
        kw = 'Test A Keyword'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, object_name, False)
        expected = [(
            '{0}\t{1}'.format(kw, object_name),
            '{0}'.format(kw)
        )]
        self.assertEqual(kw_tuple, expected)
        object_name = 'LibNoClass'
        prefix = 'librarykeyword'
        kw1 = 'Library Keyword 1'
        kw2 = 'Library Keyword 2'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, object_name, False)
        expected = [
            (
                '{0}\t{1}'.format(kw1, object_name),
                '{0}{1}arg1'.format(kw1, '\n...' + RF_CELL)
            ),
            (
                '{0}\t{1}'.format(kw2, object_name),
                '{0}{1}arg1{1}arg2'.format(kw2, '\n...' + RF_CELL)
            ),
        ]
        self.assertEqual(kw_tuple, expected)
        object_name = 'BuiltIn'
        prefix = 'lo'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix,
                                          RF_CELL, object_name, False)
        for completion in kw_tuple:
            self.assertRegexpMatches(completion[0], object_name)

    def test_kw_create_completion_item(self):
        # kw with args
        kw = 'Run Keyword And Expect Error'
        lib = 'BuiltIn'
        kw_completion = '{0}{1}expected_error{1}name{1}*args'.format(
            kw, '\n...    ')
        args = ['expected_error', 'name', '*args']
        completion = create_kw_completion_item(kw, args, RF_CELL, lib, False)
        trigger = '{0}\t{1}'.format(kw, lib)
        expected = (trigger, kw_completion)
        self.assertEqual(completion, expected)
        # kw not args
        kw = 'Unselect Frame'
        lib = 'Selenium2Library'
        completion = create_kw_completion_item(kw, [], RF_CELL, lib, False)
        trigger = '{0}\t{1}'.format(kw, lib)
        expected = (trigger, kw)
        self.assertEqual(completion, expected)

    def test_kw_create_completion_item_sinlge_line(self):
        # kw with args
        kw = 'Run Keyword And Expect Error'
        lib = 'BuiltIn'
        kw_completion = '{0}{1}expected_error{1}name{1}*args'.format(
            kw, '    ')
        args = ['expected_error', 'name', '*args']
        completion = create_kw_completion_item(kw, args, RF_CELL, lib, True)
        trigger = '{0}\t{1}'.format(kw, lib)
        expected = (trigger, kw_completion)
        self.assertEqual(completion, expected)
        # kw not args
        kw = 'Unselect Frame'
        lib = 'Selenium2Library'
        completion = create_kw_completion_item(kw, [], RF_CELL, lib, True)
        trigger = '{0}\t{1}'.format(kw, lib)
        expected = (trigger, kw)
        self.assertEqual(completion, expected)

    def test_create_variable_completion_item(self):
        scalar = '${var}'
        # Mode is True == $
        expected = (scalar, '{0}'.format(scalar[1:]))
        result = create_var_completion_item(scalar, True)
        self.assertEqual(result, expected)
        # Mode is False == {} or {
        expected = (scalar, '{0}'.format(scalar[2:-1]))
        result = create_var_completion_item(scalar, False)
        self.assertEqual(result, expected)

    def test_get_var_completion_list(self):
        vars_in_completion = self.vars_in_test_a
        var_l = []
        for var in vars_in_completion:
            if var.startswith('$'):
                var_l.append((var, var[1:]))
            else:
                var_l.append((var, var))
        result = get_var_completion_list(self.test_a_index, '$', '')
        result = sorted(result, key=lambda v: v[0])
        var_l = sorted(var_l, key=lambda v: v[0])
        for e, r in zip(result, var_l):
            self.assertEqual(r, e)
        self.assertEqual(len(result), len(var_l))
        # Single var
        result = get_var_completion_list(self.test_a_index, '${RESO}', '')
        self.assertEqual(result, [('${RESOURCE_A}', 'RESOURCE_A')])
        result = get_var_completion_list(self.test_a_index, '${reso}', '')
        self.assertEqual(result, [('${RESOURCE_A}', 'RESOURCE_A')])
        result = get_var_completion_list(self.test_a_index, '@', '')
        self.assertEqual(result, [('@{EMPTY}', '{EMPTY}'),
                                  ('@{TEST_TAGS}', '{TEST_TAGS}')])
        result = get_var_completion_list(self.test_a_index, '&', '')
        self.assertEqual(result, [('&{EMPTY}', '{EMPTY}'),
                                  ('&{SUITE_METADATA}', '{SUITE_METADATA}')])
        # No match
        result = get_var_completion_list(self.test_a_index, '${NOT_HERE', '')
        self.assertEqual(result, [])
        # Text inside of var
        result = get_var_completion_list(self.test_a_index, '${Tru}', '')
        self.assertEqual(len(result), 1)

    def test_get_var_mode(self):
        self.assertTrue(get_var_mode('$'))
        self.assertTrue(get_var_mode('@'))
        self.assertTrue(get_var_mode('&'))
        self.assertFalse(get_var_mode('${}'))
        self.assertFalse(get_var_mode('${CUR}'))

    def test_get_var_re_string(self):
        self.assertEqual(get_var_re_string('$'), '(?i)\$.*')
        self.assertEqual(get_var_re_string('${'), '(?i)\$\{.*')
        self.assertEqual(get_var_re_string('${}'), '(?i)\$\{.*\}')
        self.assertEqual(get_var_re_string('${var}'), '(?i)\$\{.*v.*a.*r.*\}')
        self.assertEqual(get_var_re_string('@{var}'), '(?i)\@\{.*v.*a.*r.*\}')
        self.assertEqual(get_var_re_string('&{var}'), '(?i)\&\{.*v.*a.*r.*\}')
        expected = '(?i)\\@\\{.*l.*i.*\}'
        self.assertEqual(get_var_re_string('@{li}'), expected)

    def test_check_prefix(self):
        prefix = ''
        line = '    ${}'
        column = 6
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, '${}')
        self.assertEqual(result_column, 2)

        prefix = 'C'
        line = '    ${C}'
        column = 7
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, '${C}')
        self.assertEqual(result_column, 3)

        prefix = 'Run'
        line = '    Run'
        column = 7
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, prefix)
        self.assertEqual(result_column, 3)

        prefix = 'C'
        line = '    ${CURDIR}${C}${PATH_TO}'
        column = 16
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, '${C}')
        self.assertEqual(result_column, 3)

        prefix = ''
        line = '    ${CURDIR}${}'
        column = 15
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, '${}')
        self.assertEqual(result_column, 2)

        prefix = ''
        line = '    $'
        column = len(line)
        result_prefix, result_column = check_prefix(line, column, prefix)
        self.assertEqual(result_prefix, '$')
        self.assertEqual(result_column, 1)

    def test_arguments_defaults(self):
        prefix = 'ResourceBKeyword3ManyArg'
        result = get_completion_list(
            self.test_b_index, prefix, len(prefix), None, False, RF_CELL)
        expected = [(
            'Resource B Keyword 3 Many Args\tresource_b',
            (
                'Resource B Keyword 3 Many Args\n'
                '...    arg1=${True}\n'
                '...    arg2\n'
                '...    arg3=${False}'
            )
        )]
        self.assertEqual(result, expected)

    def test_lib_with_name(self):
        prefix = 'othername'
        result = get_completion_list(
            self.test_b_index, prefix, len(prefix), None, False, RF_CELL
        )
        expected = [('OtherNameLib\tOtherNameLib', 'OtherNameLib.')]
        self.assertEqual(result, expected)

    def test_kw_from_lib_with_name(self):
        prefix = 'Keyword'
        object_name = 'OtherNameLib'
        result = get_completion_list(
            self.test_b_index, prefix, len(prefix), object_name, False, RF_CELL
        )
        expected = [(
            (
                'Keyword Which Also Has Really Long Name But Not As Long '
                'The Class Name By ${argument} In Keyword\tOtherNameLib'
            ),
            (
                'Keyword Which Also Has Really Long Name But Not As Long '
                'The Class Name By \\${argument} In Keyword'
            )
        )]
        self.assertEqual(result, expected)

    def test_with_name_in_import(self):
        result = add_with_name('WIT', None, RF_CELL)
        self.assertEqual(result, ('WITH NAME\tWITH NAME', 'WITH NAME'))
        result = add_with_name('NOT', None, RF_CELL)
        self.assertEqual(result, None)
        result = add_with_name('wi', None, RF_CELL)
        self.assertEqual(result, None)

    @property
    def vars_in_test_a(self):
        return [
            '${TEST_A}',
            '${COMMON_VARIABLE_1}',
            '${COMMON_VARIABLE_2}',
            '${RESOURCE_A}',
            '${/}',
            '${:}',
            '${\\n}',
            '${CURDIR}',
            '${DEBUG_FILE}',
            '${EMPTY}',
            '${EXECDIR}',
            '${False}',
            '${LOG_FILE}',
            '${LOG_LEVEL}',
            '${None}',
            '${null}',
            '${OUTPUT_DIR}',
            '${OUTPUT_FILE}',
            '${PREV_TEST_MESSAGE}',
            '${PREV_TEST_NAME}',
            '${PREV_TEST_STATUS}',
            '${REPORT_FILE}',
            '${SPACE}',
            '${SUITE_DOCUMENTATION}',
            '${SUITE_NAME}',
            '${SUITE_SOURCE}',
            '${TEMPDIR}',
            '${TEST_DOCUMENTATION}',
            '${TEST_NAME}',
            '${True}'
        ]
