import unittest
from collections import OrderedDict
from queue.queue import ParsingQueue


class TestLibraryParsingQueue(unittest.TestCase):
    """Unit test for test data parsing queue"""

    def setUp(self):
        self.queue = ParsingQueue()
        self.expected = OrderedDict()
        self.not_scanned = {'scanned': False}
        self.lib = {'type': 'library'}
        self.test = {'type': 'test_suite'}
        self.none = {'type': None}
        self.resource = {'type': 'resource'}
        self.no_args = {'args': None}

    def update_expected(self, dict1):
        old = self.expected
        self.expected = OrderedDict(list(dict1.items()) + list(old.items()))

    def test_errors(self):
        queue = ParsingQueue()
        self.assertEqual(
            queue.get(),
            {})
        with self.assertRaises(ValueError):
            queue.add('BuiltIn', 'invalid', None)
        with self.assertRaises(KeyError):
            queue.set('NotHere')
        with self.assertRaises(TypeError):
            queue.add('BuiltIn', 'library')

    def test_queue_creation(self):
        self.assertEqual(
            self.queue.queue,
            self.expected)

    def test_adding_library(self):
        self.add_builtin()
        self.assertEqual(
            self.queue.queue,
            self.expected)
        # Adding lib second time should not add item to the queue
        self.queue.add('BuiltIn', 'library', None)
        self.assertEqual(
            self.queue.queue,
            self.expected)

    def test_adding_test_data(self):
        self.add_test_data()
        self.assertEqual(
            self.queue.queue,
            self.expected)
        self.add_resource()
        self.assertEqual(
            self.queue.queue,
            self.expected)

    def test_get_from_queue(self):
        self.add_builtin()
        self.add_test_data()
        self.add_resource()
        data = self.queue.get()
        except_data = self.expected.popitem(last=False)
        except_data[1]['scanned'] = False
        self.assertEqual(data, except_data)
        except_data[1]['scanned'] = 'queued'
        self.expected['resource.robot'] = except_data[1]
        self.assertEqual(self.queue.queue, self.expected)
        # Adding lib second time should not add item to the queue
        self.queue.add('BuiltIn', 'library', None)
        self.assertEqual(self.queue.queue, self.expected)

    def test_mark_item_as_scanned(self):
        self.add_builtin()
        self.add_test_data()
        self.add_resource()
        except_data = self.queue.get()
        self.queue.set('resource.robot')
        self.expected.popitem(last=False)
        except_data[1]['scanned'] = True
        self.expected['resource.robot'] = except_data[1]
        self.assertEqual(self.queue.queue, self.expected)
        # Adding scanned item should not change the item
        self.queue.add('resource.robot', 'resource', None)
        self.assertEqual(self.queue.queue, self.expected)

    def test_add_with_args(self):
        self.queue.add('SomeLib', 'library', [1, 2, 3])
        self.assertEqual(
            self.queue.queue,
            OrderedDict([(
                'SomeLib',
                {'scanned': False, 'type': 'library', 'args': [1, 2, 3]})]))

    def test_clear_queue(self):
        self.add_test_data()
        self.add_resource()
        self.add_builtin()
        self.assertGreater(len(self.queue.queue), 2)
        self.queue.clear_queue()
        self.assertEqual(len(self.queue.queue), 0)

    def test_add_dublicates(self):
        """Duplicates"""
        self.queue.add('/path/to/robot.robot', None, None)
        self.assertEqual(len(self.queue.queue), 1)
        self.queue.add('/path/to/robot.robot', None, None)
        self.assertEqual(len(self.queue.queue), 1)
        self.queue.add('/path/to/robot.robot', 'resource', None)
        self.assertEqual(len(self.queue.queue), 1)

    def test_force_set(self):
        self.add_test_data()
        self.add_builtin()
        self.add_resource()
        self.assertEqual(len(self.queue.queue), 3)
        resources = ['resource1.robot', 'resource2.robot', 'resource3.robot']
        self.queue.force_set(resources[0])
        self.queue.force_set(resources[1])
        self.queue.force_set(resources[2])
        self.assertEqual(len(self.queue.queue), 6)
        first_index = 3
        status = {'scanned': True, 'type': None, 'args': None}
        for index, key in enumerate(self.queue.queue):
            if key in resources:
                self.assertEqual(index, first_index)
                first_index += 1
                self.assertEqual(self.queue.queue[key], status)
        resource = 'resource.robot'
        self.queue.force_set(resource)
        for index, key in enumerate(self.queue.queue):
            if key in resource:
                self.assertEqual(self.queue.queue[key], status)
                self.assertEqual(index, 5)

    def add_builtin(self):
        tmp = OrderedDict({})
        tmp['BuiltIn'] = self.join_dict(
            self.not_scanned, self.lib, self.no_args)
        self.update_expected(tmp)
        self.queue.add('BuiltIn', 'library', None)

    def add_test_data(self):
        tmp = OrderedDict({})
        tmp['some.robot'] = self.join_dict(
            self.not_scanned, self.none, self.no_args)
        self.update_expected(tmp)
        self.queue.add('some.robot', None, None)

    def add_resource(self):
        tmp = OrderedDict({})
        tmp['resource.robot'] = self.join_dict(
            self.not_scanned, self.resource, self.no_args)
        self.update_expected(tmp)
        self.queue.add('resource.robot', 'resource', None)

    def join_dict(self, dict1, dict2, dict3):
        x = dict1.copy()
        x.update(dict2)
        x.update(dict3)
        return x
