import unittest
from dataparser.parser.getbuiltinvariables import GetBuiltInVariables


class TestGetBuiltInVars(unittest.TestCase):

    def test_get_builtin_vars(self):
        """Most likely this is not good idea"""
        pass
        # l = GetBuiltInVariables()
        # rf_vars = l.get_builtin_vars()
        # self.assertTrue('${EXECDIR}' in rf_vars)
        # self.assertTrue('${/}' in rf_vars)
        # self.assertTrue('@{TEST_TAGS}' in rf_vars)
