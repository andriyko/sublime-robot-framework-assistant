import unittest
import env
import os
import shutil
import subprocess
from time import sleep
from queue.scanner import Scanner
from test_runner_for_scanner import run_process


class TestRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_dir = os.path.join(
            env.RESOURCES_DIR,
            'db_dir'
        )
        cls.workspace = os.path.join(env.TEST_DATA_DIR, 'suite_tree')
        scanner = Scanner()
        scanner.scan(
            cls.workspace,
            'robot',
            cls.db_dir)

    def setUp(self):
        self.index_path = os.path.join(
            env.RESULTS_DIR,
            'index_dir'
        )
        if os.path.exists(self.index_path):
            while os.path.exists(self.index_path):
                shutil.rmtree(self.index_path)
                sleep(0.1)
            os.mkdir(self.index_path)
        self.runner = os.path.join(env.SRC_DIR, 'run_index.py')
        self.index_path = os.path.join(
            env.RESULTS_DIR,
            'index_dir'
        )

    def test_index_all_runner(self):
        p_args = [
            'python',
            self.runner,
            'all',
            '--db_path',
            self.db_dir,
            '--index_path',
            self.index_path
        ]
        log_file = run_process(p_args)
        f = open(log_file)
        self.assertFalse(f.readlines())
        f.close()
        files = os.listdir(self.index_path)
        self.assertEqual(len(files), 10)
