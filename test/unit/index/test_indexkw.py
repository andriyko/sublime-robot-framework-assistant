import unittest
import env
import os
import shutil
from time import sleep
import json
from dataparser.queue.scanner import Scanner
from dataparser.index.index import Index


class TestIndexing(unittest.TestCase):

    """The content of the db_fir was created with scanner by scanning the
    TEST_DATA_DIR/suite_tree folder. If scanner is changed, db_dir must
    be recreated."""

    @classmethod
    def setUpClass(cls):
        db_dir = os.path.join(
            env.RESOURCES_DIR,
            'db_dir'
        )
        cls.suite_dir = os.path.join(
            env.TEST_DATA_DIR,
            'suite_tree'
        )
        scanner = Scanner()
        scanner.scan(
            cls.suite_dir,
            'robot',
            db_dir)

    def setUp(self):
        self.index_dir = os.path.join(
            env.RESULTS_DIR,
            'index_dir',
        )
        if os.path.exists(self.index_dir):
            while os.path.exists(self.index_dir):
                shutil.rmtree(self.index_dir)
                sleep(0.1)
            os.mkdir(self.index_dir)
        self.index = Index()
        self.test_a_robot = 'test_a.robot'
        self.test_a = os.path.join(
            self.suite_dir,
            self.test_a_robot)

    def test_kw_index_testa(self):
        self.index.index_file(self.test_a, self.index_dir)
        self.assertTrue(os.path.isfile(self.test_a))
        self.assertEqual(
            self.read_index('PATH TO INDEX FILE'),
            self.expected_test_a_index(self.test_a)
            )

    def test_kw_index_resourceb(self):
        raise ValueError('Not done')

    def test_var_index_testa(self):
        raise ValueError('Not done')

    def test_kw_shource_index_testa(self):
        raise ValueError('Not done')

    def test_kw_shource_index_testb(self):
        raise ValueError('Not done')

    def expected_test_a_index(self):
        res_kw = [
            'Resource A Keyword 1',
            'Resource A Keyword 2',
            'Common Keyword 1',
            'Common Keyword 2']
        return res_kw + self.read_kw_from_file(
            os.path.join(self.suite_dir, 'test_a.robot'))

    def read_kw_from_file(self, f_name):
        f = open(f_name)
        data = json.load(f)
        f.close()
        return data['keywords'].keys()

    def read_index(self, f_name):
        f = open(f_name)
        data = json.load(f)
        f.close()
        return data
