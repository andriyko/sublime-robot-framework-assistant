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
        self.builtin = ('BuiltIn', {'scanned': False, 'type': 'library'})
        self.some = ('some.robot', {'scanned': False, 'type': None})
        self.resource = (
            'resource.robot',
            {'scanned': False, 'type': 'resource'}
            )

    def test_errors(self):
        with self.assertRaises(EnvironmentError):
            self.scanner.scan(
                '/not/here',
                'robot',
                self.db_dir
                )
        curr_file = os.path.realpath(__file__)
        with self.assertRaises(EnvironmentError):
            self.scanner.scan(
                self.workspace,
                'robot',
                curr_file
                )

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
            {'scanned': False, 'type': None}
            )

    def test_get_item(self):
        self.add_test_data()
        data1 = self.scanner.get_item()
        self.assertEqual(data1, self.builtin)
        data2 = self.scanner.get_item()
        self.assertEqual(data2, self.some)

    def test_get_item_last_item(self):
        self.add_test_data()
        for index in range(3):
            data = self.scanner.get_item()
        self.assertEqual(data, self.resource)
        data = self.scanner.get_item()
        self.assertEqual(data, {})

    def test_db_created(self):
        print self.db_dir
        self.scanner.scan(
            self.workspace,
            'robot',
            self.db_dir
            )
        self.assertGreater(
            len(os.listdir(self.db_dir)),
            2)

    def add_test_data(self):
        self.scanner.queue.add('BuiltIn', 'library')
        self.scanner.queue.add('some.robot', None)
        self.scanner.queue.add('resource.robot', 'resource')
