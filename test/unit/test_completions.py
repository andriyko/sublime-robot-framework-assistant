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


class TestCompletions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_a_index = path.join(
            env.RESOURCES_DIR,
            'current_view.json')

    def test_get_completion_list(self):
        prefix = 'Run'
        result = get_completion_list(self.test_a_index, prefix, '')
        self.assertEqual(len(result), 39)
        result = get_completion_list(self.test_a_index, '$', '')
        self.assertEqual(len(result), 28)

    def test_get_kw_re_string(self):
        re_string = get_kw_re_string('1')
        self.assertEqual(re_string, '(?i)(.*1)')
        re_string = get_kw_re_string('123')
        self.assertEqual(re_string, '(?i)(.*1.*2.*3)')
        re_string = get_kw_re_string(123)
        self.assertEqual(re_string, '(?i)(.*1.*2.*3)')

    def test_get_kw_completion_list_count(self):
        prefix = 'Run'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix)
        self.assertEqual(len(kw_tuple), 39)
        prefix = 'RunKeY'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix)
        self.assertEqual(len(kw_tuple), 19)
        prefix = 'BUI'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix)
        self.assertEqual(len(kw_tuple), 13)

    def test_get_kw_completion_list_structure(self):
        prefix = 'Run'
        kw_tuple = get_kw_completion_list(self.test_a_index, prefix)
        expected = (
            'Run Keyword And Expect Error\tBuiltIn',
            'Run Keyword And Expect Error'
        )
        self.assertEqual(kw_tuple[0], expected)
        expected = (
            'Run And Return Rc\tOperatingSystem',
            'Run And Return Rc')
        self.assertEqual(kw_tuple[-1], expected)

    def test_kw_create_completion_item(self):
        kw = 'Run Keyword And Expect Error'
        lib = 'BuiltIn'
        completion = create_kw_completion_item(kw, lib)
        trigger = '{0}\t{1}'.format(kw, lib)
        expected = (trigger, kw)
        self.assertEqual(completion, expected)

    def test_create_variable_completion_item(self):
        scalar = '${var}'
        # Mode 1
        expected = (scalar, '{0}'.format(scalar[1:]))
        result = create_var_completion_item(scalar, 1)
        self.assertEqual(result, expected)
        # Mode 2
        expected = (scalar, '{0}'.format(scalar[2:5]))
        result = create_var_completion_item(scalar, 2)
        self.assertEqual(result, expected)
        # Mode 3
        expected = (scalar, '{0}'.format(scalar[2:]))
        result = create_var_completion_item(scalar, 3)
        self.assertEqual(result, expected)

    def test_get_var_completion_list(self):
        vars_in_completion = [
            '${/}',
            '${:}',
            '${\\n}',
            '${DEBUG_FILE}',
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
            '${True}',
            '${TEST_A}',
            '${COMMON_VARIABLE_1}',
            '${COMMON_VARIABLE_2}',
            '${RESOURCE_A}'
        ]
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
        result = get_var_completion_list(self.test_a_index, '${RESO', '')
        self.assertEqual(result, [('${RESOURCE_A}', 'RESOURCE_A}')])
        result = get_var_completion_list(self.test_a_index, '${reso', '')
        self.assertEqual(result, [('${RESOURCE_A}', 'RESOURCE_A}')])
        result = get_var_completion_list(self.test_a_index, '@', '')
        self.assertEqual(result, [('@{TEST_TAGS}', '{TEST_TAGS}')])
        result = get_var_completion_list(self.test_a_index, '&', '')
        self.assertEqual(result, [('&{SUITE_METADATA}', '{SUITE_METADATA}')])
        # No match
        result = get_var_completion_list(self.test_a_index, '${NOT_HERE', '')
        self.assertEqual(result, [])

    def test_text_before_var(self):
        result = get_var_completion_list(self.test_a_index, 'text@', '')
        self.assertEqual(result, [('@{TEST_TAGS}', '{TEST_TAGS}')])
        result = get_var_completion_list(self.test_a_index, 'text@{', '')
        self.assertEqual(result, [('@{TEST_TAGS}', 'TEST_TAGS}')])
        result = get_var_completion_list(self.test_a_index, 'text@', '')
        self.assertEqual(result, [('@{TEST_TAGS}', '{TEST_TAGS}')])

    def test_get_var_mode(self):
        result = get_var_mode('$', '')
        self.assertEqual(result, 1)
        result = get_var_mode('${', '}')
        self.assertEqual(result, 2)
        result = get_var_mode('${', '')
        self.assertEqual(result, 3)

    def test_get_var_re_string(self):
        var = '${var}'
        self.assertEqual(get_var_re_string(var), '(?i)\\{0}'.format(var))
        var = '@{var}'
        self.assertEqual(get_var_re_string(var), '(?i)\\{0}'.format(var))
        var = '&{var}'
        self.assertEqual(get_var_re_string(var), '(?i)\\{0}'.format(var))
        expected = '(?i)\\$\{.*v.*a.*r'
        self.assertEqual(get_var_re_string('${var'), expected)
        self.assertEqual(get_var_re_string('var_subtition${var'), expected)
        expected = '(?i)\\$\\{'
        self.assertEqual(get_var_re_string('${'), expected)
        expected = '(?i)\\@\\{'
        self.assertEqual(get_var_re_string('@{'), expected)
        expected = '(?i)\\&\\{'
        self.assertEqual(get_var_re_string('&{'), expected)
        expected = '(?i)\\@\\{.*l.*i'
        self.assertEqual(get_var_re_string('@{li'), expected)
        self.assertEqual(get_var_re_string('var_subtition@{li'), expected)
