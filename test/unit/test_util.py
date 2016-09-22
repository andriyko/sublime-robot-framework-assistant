import unittest
from utils.util import kw_equals_kw_candite


class TestUtil(unittest.TestCase):

    def test_kw_equals_kw_candite(self):
        kw1 = 'My Long Keyword'
        kw2 = '.My Long Keyword'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
        kw2 = 'Not Same'
        self.assertFalse(kw_equals_kw_candite(kw1, kw2))
        kw1 = 'My Long Keyword'
        kw2 = '.my long keyword'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
        kw1 = 'My Long Keyword'
        kw2 = '.my_LONG_keyword'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
        kw1 = 'My Long Keyword'
        kw2 = '.myLONGkeyword'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))

    def test_embedded_arg_kw(self):
        kw1 = 'Embedding arg To Keyword Name'
        kw2 = 'Embedding ${arg} To Keyword Name'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
        kw1 = 'EMBEDDING_ARG_TO_KEYWORD_NAME'
        kw2 = 'Embedding ${arg} To Keyword Name'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
        kw1 = 'embedding_arg_to_keyword_name'
        kw2 = 'Embedding ${arg} To Keyword Name'
        self.assertTrue(kw_equals_kw_candite(kw1, kw2))
