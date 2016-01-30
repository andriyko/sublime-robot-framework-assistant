import unittest
import env
import os
import shutil
import subprocess
from time import sleep


class TestRunnerForScanner(unittest.TestCase):

    def setUp(self):
        self.db_dir = os.path.join(
            env.RESULTS_DIR,
            'scanner',
            'db_dir'
        )
        self.real_suite = os.path.join(
            env.TEST_DATA_DIR,
            'suite_tree')
        if os.path.exists(self.db_dir):
            while os.path.exists(self.db_dir):
                shutil.rmtree(self.db_dir)
                sleep(0.1)
            os.mkdir(self.db_dir)
            sleep(0.1)
        self.workspace = env.TEST_DATA_DIR
        self.runner = os.path.join(env.SRC_DIR, 'run_scanner.py')

    def test_scan_all(self):
        p_args = [
            'python',
            self.runner,
            'all',
            '--workspace',
            self.workspace,
            '--extension',
            'robot',
            '--db_path',
            self.db_dir]
        self.run_process(p_args)
        files = os.listdir(self.db_dir)
        self.assertEqual(len(files), 22)

    def test_scan_errors(self):
        p_args = [
            'python',
            self.runner,
            'all',
            '--db_path',
            self.db_dir]
        log_file = self.run_process(p_args)
        f = open(log_file)
        self.assertTrue(f.readlines()[-1].startswith('ValueError'))
        f.close()

        p_args = [
            'python',
            self.runner,
            'all',
            '--workspace',
            self.workspace,
            '--db_path',
            self.db_dir]
        log_file = self.run_process(p_args)
        f = open(log_file)
        self.assertTrue(f.readlines()[-1].startswith('ValueError'))
        f.close()

        p_args = [
            'python',
            self.runner,
            'single',
            '--db_path',
            self.db_dir]
        log_file = self.run_process(p_args)
        f = open(log_file)
        self.assertTrue(f.readlines()[-1].startswith('ValueError'))
        f.close()

    def run_process(self, p_args):
        log_file = open(os.path.join(env.RESULTS_DIR, 'popen.log'), 'w')
        p = subprocess.Popen(
            p_args,
            stderr=subprocess.STDOUT,
            stdout=log_file
        )
        p.wait()
        log_file.name
        log_file.close()
        return log_file.name
