import unittest
import env
import os
import shutil
import hashlib
from time import sleep
import json
from queue.scanner import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()
        self.db_dir = os.path.join(
            env.RESULTS_DIR,
            'scanner',
            'db_dir'
        )
        self.real_suite = os.path.join(
            env.TEST_DATA_DIR,
            'real_suite')
        if os.path.exists(self.db_dir):
            while os.path.exists(self.db_dir):
                shutil.rmtree(self.db_dir)
                sleep(0.1)
            os.mkdir(self.db_dir)
        self.workspace = env.TEST_DATA_DIR
        self.builtin = (
            'BuiltIn',
            {
                'scanned': False,
                'type': 'library',
                'args': []
            }
        )
        self.some = (
            'some.robot',
            {
                'scanned': False,
                'type': None,
                'args': []
            }
        )
        self.resource = (
            'resource.robot',
            {
                'scanned': False,
                'type': 'resource',
                'args': []
            }
        )
        self.xml_libs = os.path.join(
            env.RESOURCES_DIR,
            'library'
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
            self.real_suite,
            'robot',
            self.db_dir
        )
        self.assertEqual(len(self.scanner.queue.queue), 10)
        key = os.path.join(
            self.real_suite,
            'resource',
            'reosurce2',
            'real_suite_resource.robot'
        )
        key = os.path.normcase(key)
        self.assertEqual(
            self.scanner.queue.queue[key],
            {'scanned': True, 'type': None, 'args': None}
        )

    def test_add_libraries_queue(self):
        libs = [{'library_name': u'OperatingSystem',
                 'library_alias': None,
                 'library_arguments': None,
                 'library_path': None},
                {'library_name': u'Process',
                 'library_alias': None,
                 'library_arguments': None,
                 'library_path': None}]
        self.scanner.add_libraries_queue(libs)
        self.assertEqual(len(self.scanner.queue.queue), 2)

    def test_get_item(self):
        self.add_test_data()
        data1 = self.scanner.get_item()
        self.assertEqual(data1, self.resource)
        data2 = self.scanner.get_item()
        self.assertEqual(data2, self.some)

    def test_get_item_last_item(self):
        self.add_test_data()
        for index in range(3):
            data = self.scanner.get_item()
        self.assertEqual(data, self.builtin)
        data = self.scanner.get_item()
        self.assertEqual(data, {})

    def test_db_created(self):
        self.scanner.scan(
            self.real_suite,
            'robot',
            self.db_dir
        )
        self.assertEqual(len(os.listdir(self.db_dir)), 8)

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
        item = (library, {'scanned': False, 'type': 'library', 'args': None})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)

    def test_parse_variable_file(self):
        var = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_variable_file.py'
        )
        item = (var, {
            'scanned': False,
            'type': 'variable_file',
            'args': []})
        data = self.scanner.parse_all(item)
        self.assertNotEqual(data, None)

    def test_add_imports_from_resource(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            4
        )

    def test_scanning_same_resource_two_times_does_not_change_queue(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            4
        )
        self.scanner.add_to_queue(data)
        self.assertEqual(len(
            self.scanner.queue.queue),
            4
        )

    def test_put_item_to_db(self):
        item = self.create_resource_item()
        data = self.scanner.parse_all(item)
        self.scanner.put_item_to_db(data, self.db_dir)
        f_name = self.f_name(data, self.db_dir)
        self.assertTrue(os.path.isfile(f_name))

    def test_put_items_to_db(self):
        item1 = self.create_resource_item()
        data1 = self.scanner.parse_all(item1)
        self.scanner.put_item_to_db(data1, self.db_dir)
        item2 = self.create_resource_item2()
        data2 = self.scanner.parse_all(item2)
        self.scanner.put_item_to_db(data2, self.db_dir)
        file1 = self.f_name(data1, self.db_dir)
        self.assertTrue(os.path.isfile(file1))
        file2 = self.f_name(data2, self.db_dir)
        self.assertTrue(os.path.isfile(file2))
        f = open(file2, 'r')
        self.assertTrue(json.load(f))
        f.close()

    def test_builtin_in_queue(self):
        self.scanner.add_builtin()
        self.assertEqual(len(self.scanner.queue.queue), 1)

    def test_parse_suite_structure(self):
        workspace = self.suite_folder()
        self.scanner.scan(workspace, 'robot', self.db_dir)
        files = os.listdir(self.db_dir)
        builtin = '{0}-{1}.json'.format(
            'BuiltIn',
            hashlib.md5('BuiltIn').hexdigest())
        self.assertTrue(builtin in files)
        init = '{0}-{1}.json'.format(
            '__init__.robot',
            hashlib.md5(
                os.path.normcase(
                    os.path.join(workspace, '__init__.robot'))).hexdigest()
        )
        self.assertTrue(init in files)
        suite = '{0}-{1}.json'.format(
            'test_with_libs.robot',
            hashlib.md5(
                os.path.normcase(
                    os.path.join(
                        workspace, 'test_with_libs.robot'))).hexdigest()
        )
        self.assertTrue(suite in files)
        operatingsystem = '{0}-{1}.json'.format(
            'OperatingSystem',
            hashlib.md5('OperatingSystem').hexdigest())
        self.assertTrue(operatingsystem in files)
        operatingsystem = '{0}-{1}.json'.format(
            'Process',
            hashlib.md5('Process').hexdigest())
        self.assertTrue(operatingsystem in files)
        self.assertEqual(len(files), 6)

    def test_parse_real_suite(self):
        workspace = os.path.join(
            env.TEST_DATA_DIR,
            'suite_tree')
        self.scanner.scan(
            workspace,
            'robot',
            self.db_dir)
        files = os.listdir(self.db_dir)
        builtin = '{0}-{1}.json'.format(
            'BuiltIn',
            hashlib.md5('BuiltIn').hexdigest())
        self.assertTrue(builtin in files)
        operatingsystem = '{0}-{1}.json'.format(
            'OperatingSystem',
            hashlib.md5('OperatingSystem').hexdigest())
        self.assertTrue(operatingsystem in files)
        self.assertEqual(len(files), 14)

    def test_single_file_scan(self):
        self.assertEqual(len(os.listdir(self.db_dir)), 0)
        self.scanner.scan_single_file(self.real_suite_robot_path, self.db_dir)
        self.assertEqual(len(os.listdir(self.db_dir)), 1)
        self.scanner.scan_single_file(self.real_suite_robot_path, self.db_dir)
        self.assertEqual(len(os.listdir(self.db_dir)), 1)
        self.scanner.scan_single_file(
            self.real_suite_resource_robot_path,
            self.db_dir
        )
        self.assertEqual(len(os.listdir(self.db_dir)), 2)

    def test_add_xml_library(self):
        self.assertEqual(len(self.scanner.queue.queue), 0)
        self.scanner.add_xml_libraries(self.xml_libs)
        self.assertEqual(len(self.scanner.queue.queue), 2)

    def test_scan_with_xml_lib(self):
        scaner = Scanner(self.xml_libs)
        scaner.scan(
            self.real_suite,
            'robot',
            self.db_dir
        )
        self.assertEqual(len(os.listdir(self.db_dir)), 10)

    @property
    def real_suite_robot_path(self):
        return os.path.join(self.real_suite, 'test', 'real_suite.robot')

    @property
    def real_suite_resource_robot_path(self):
        return os.path.join(
            self.real_suite,
            'resource',
            'resource1',
            'real_suite_resource.robot'
        )

    def suite_folder(self):
        return os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'init_structure'
        )

    def create_resource_item(self):
        resource = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_resource.robot'
        )
        return (resource, {'scanned': False, 'type': 'resource', 'args': None})

    def create_resource_item2(self):
        resource = os.path.join(
            env.RESOURCES_DIR,
            'test_data',
            'simple_resrouce2.robot'
        )
        return (resource, {'scanned': False, 'type': 'resource', 'args': None})

    def add_test_data(self):
        self.scanner.queue.add('BuiltIn', 'library', [])
        self.scanner.queue.add('some.robot', None, [])
        self.scanner.queue.add('resource.robot', 'resource', [])

    def f_name(self, data, db_dir):
        file_name = '{realname}-{md5}.json'.format(
            realname=os.path.basename(data['file_path']),
            md5=hashlib.md5(data['file_path']).hexdigest()
        )
        return os.path.join(db_dir, file_name)
