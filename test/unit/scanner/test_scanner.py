import unittest
import env
import os
import shutil
import hashlib
from time import sleep
import json
from dataparser.queue.scanner import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()
        self.db_dir = os.path.join(
            env.RESULTS_DIR,
            'scanner',
            'db_dir'
        )
        if os.path.exists(self.db_dir):
            shutil.rmtree(self.db_dir)
            while os.path.exists(self.db_dir):
                sleep(0.1)
            os.mkdir(self.db_dir)
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

    def test_parse_all_rf(self):
        test_suite = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_test.robot'
            )
        item = (test_suite, {'scanned': False, 'type': None})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)
        resource = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_resource.robot'
            )
        item = (resource, {'scanned': False, 'type': 'resource'})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)

    def test_parse_all_library(self):
        library = os.path.join(
            env.RESOURCES_DIR,
            'library',
            'MyLibrary.py'
            )
        item = (library, {'scanned': False, 'type': 'library'})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)

    def test_parse_variable_file(self):
        var = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_variable_file.py'
            )
        item = (var, {'scanned': False, 'type': 'variable'})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)

    def test_add_imports_from_resource(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            3
            )

    def test_scanning_same_resource_two_times_does_not_change_qyueue(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            3
            )
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            3
            )

    def test_put_item_to_db(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.put_item_to_db(data, self.db_dir)
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.db_dir,
                    hashlib.md5(data['file_path']).hexdigest() + '.json'
                    )
                )
            )

    def test_put_items_to_db(self):
        item1 = self.create_resource_item()
        data1 = self.scanner.parse_all(item1)
        self.scanner.put_item_to_db(data1, self.db_dir)
        item2 = self.create_resource_item2()
        data2 = self.scanner.parse_all(item2)
        self.scanner.put_item_to_db(data2, self.db_dir)
        file1 = os.path.join(
            self.db_dir,
            hashlib.md5(data1['file_path']).hexdigest() + '.json'
            )
        self.assertTrue(os.path.isfile(file1))
        file2 = os.path.join(
                self.db_dir,
                hashlib.md5(data2['file_path']).hexdigest() + '.json'
                )
        self.assertTrue(os.path.isfile(file2))
        f = open(file2, 'r')
        self.assertTrue(json.load(f))
        f.close()

    def create_resource_item(self):
        resource = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_resource.robot'
            )
        return (resource, {'scanned': False, 'type': 'resource'})

    def create_resource_item2(self):
        resource = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_resrouce2.robot'
            )
        return (resource, {'scanned': False, 'type': 'resource'})

    def add_test_data(self):
        self.scanner.queue.add('BuiltIn', 'library')
        self.scanner.queue.add('some.robot', None)
        self.scanner.queue.add('resource.robot', 'resource')
