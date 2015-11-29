import unittest
from collections import OrderedDict
from dataparser.queue.queue import ParsingQueue


class TestLibraryParsingQueue(unittest.TestCase):
    """Unit test for test data parsing queue"""

    def setUp(self):
        self.queue = ParsingQueue()
        self.expected = OrderedDict()
        self.status = {'scanned': False}

    def test_adding(self):
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('BuiltIn')
        self.expected['BuiltIn'] = self.status
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('BuiltIn')
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('some_resource.robot')
        self.expected['some_resource.robot'] = self.status
        self.assertEqual(
            self.queue.queue,
            self.expected)

    def test_get(self):
        self.queue.add('BuiltIn')
        self.queue.add('some_resource.robot')
        self.expected['BuiltIn'] = self.status
        self.expected['some_resource.robot'] = self.status
        self.assertEqual(
            self.queue.get(),
            self.expected.popitem(last=False))
        self.assertEqual(
            self.queue.get(),
            self.expected.popitem(last=False))
        self.assertEqual(
            self.queue.get(),
            {})

    def test_udate(self):
        self.queue.add('BuiltIn')
        self.expected['BuiltIn'] = self.status
        self.assertEqual(
            self.queue.queue,
            self.expected)
        self.queue.update('BuiltIn')
        status = {'scanned': True}
        self.expected['BuiltIn'] = status
        self.assertEqual(
            self.queue.queue,
            self.expected)
        self.queue.update('BuiltIn')
        self.assertEqual(
            self.queue.queue,
            self.expected)
        self.queue.update('some_resource.robot')
        self.expected['some_resource.robot'] = status
        self.assertEqual(
            self.queue.queue,
            self.expected)
