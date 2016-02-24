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


class TestCompletions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_a_index = path.join(
            env.RESOURCES_DIR,
            'index-test_a.robot-41883aa9e5af28925d37eba7d2313d57.json')

    def test_get_completion_list(self):
        prefix = 'Run'
        result = get_completion_list(self.test_a_index, prefix)
        self.assertEqual(len(result), 39)
        result = get_completion_list(self.test_a_index, '$')
        self.assertEqual(len(result), 4)

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
            'run_keyword_and_expect_error\tBuiltIn',
            'Run Keyword And Expect Error'
        )
        self.assertEqual(kw_tuple[0], expected)
        expected = (
            'run_and_return_rc\tOperatingSystem',
            'Run And Return Rc')
        self.assertEqual(kw_tuple[-1], expected)

    def test_kw_create_completion_item(self):
        kw = 'run_keyword_and_expect_error'
        lib = 'BuiltIn'
        completion = create_kw_completion_item(kw, lib)
        trigger = '{0}\t{1}'.format(kw, lib)
        kw = kw.replace('_', ' ').title()
        expected = (trigger, kw)
        self.assertEqual(completion, expected)

    def test_create_variable_completion_item(self):
        scalar = '${var}'
        expected = (scalar, '\{0}'.format(scalar))
        result = create_var_completion_item(scalar)
        self.assertEqual(result, expected)

    def test_get_var_completion_list(self):
        var_l = [
            '${TEST_A}',
            '${COMMON_VARIABLE_1}',
            '${COMMON_VARIABLE_2}',
            '${RESOURCE_A}'
        ]
        var_l = [(i, '\{0}'.format(i)) for i in var_l]
        result = get_var_completion_list(self.test_a_index, '$')
        self.assertEqual(result, var_l)
        # Single var
        result = get_var_completion_list(self.test_a_index, '${T')
        self.assertEqual(result, [('${TEST_A}', '\${TEST_A}')])
        result = get_var_completion_list(self.test_a_index, '${t')
        self.assertEqual(result, [('${TEST_A}', '\${TEST_A}')])
        # No match
        result = get_var_completion_list(self.test_a_index, '${NOT_HERE')
        self.assertEqual(result, [])

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
