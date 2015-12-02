import unittest
import env
import os
from dataparser.queue.scanner import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()
        self.db_dir = os.path.join(
            env.RESULTS_DIR,
            'scanner',
            'db_dir'
        )
        self.workspace = env.TEST_DATA_DIR

    def test_queue_populated(self):
        self.scanner.scan(
            self.workspace,
            'robot',
            self.db_dir
            )
        self.assertGreater(len(self.scanner.queue.queue), 2)
        key = os.path.join(self.workspace, 'simple_test.robot')
        self.assertEqual(
            self.scanner.queue.queue[key],
            {'scanned': False}
            )

    def test_db_created(self):
        self.scanner.scan(
            self.workspace,
            'robot',
            self.db_dir
            )
        self.assertGreater(
            len(os.listdir(self.db_dir)),
            2)
