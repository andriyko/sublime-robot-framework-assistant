import unittest
import env
import os
import shutil
import re
from time import sleep
from queue.scanner import Scanner
from test_runner_for_scanner import run_process


class TestRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_dir = os.path.join(
            env.RESULTS_DIR,
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
        lines = self.clean_info_messages(log_file)
        self.assertFalse(lines)
        files = os.listdir(self.index_path)
        self.assertEqual(len(files), 14)

    def test_index_single(self):
        db_files = os.listdir(self.db_dir)
        p_args = [
            'python',
            self.runner,
            'single',
            '--db_path',
            self.db_dir,
            '--db_table',
            db_files[0],
            '--index_path',
            self.index_path
        ]
        self.assertEqual(len(os.listdir(self.index_path)), 0)
        log_file = run_process(p_args)
        lines = self.clean_info_messages(log_file)
        self.assertFalse(lines)
        self.assertEqual(len(os.listdir(self.index_path)), 1)
        log_file = run_process(p_args)
        lines = self.clean_info_messages(log_file)
        self.assertFalse(lines)
        self.assertEqual(len(os.listdir(self.index_path)), 1)
        p_args = [
            'python',
            self.runner,
            'single',
            '--db_path',
            self.db_dir,
            '--db_table',
            db_files[1],
            '--index_path',
            self.index_path
        ]
        log_file = run_process(p_args)
        lines = self.clean_info_messages(log_file)
        self.assertFalse(lines)
        self.assertEqual(len(os.listdir(self.index_path)), 2)

    def clean_info_messages(self, log_file):
        f = open(log_file)
        # Strip way S2L info messages
        pattern = re.compile(
            r'(?im)^INFO:'
        )
        lines = []
        for line in f.readlines():
            if not pattern.search(line):
                lines.append(line)
        f.close()
        return lines
