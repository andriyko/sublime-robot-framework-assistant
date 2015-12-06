import unittest
from collections import OrderedDict
from dataparser.queue.queue import ParsingQueue


class TestLibraryParsingQueue(unittest.TestCase):
    """Unit test for test data parsing queue"""

    def setUp(self):
        self.queue = ParsingQueue()
        self.expected = OrderedDict()
        self.status = {'scanned': False}
        self.lib = {'type': 'library'}
        self.test = {'type': 'test_suite'}
        self.resource = {'type': 'resource'}

    def _join_dict(self, dict1, dict2):
        x = dict1.copy()
        x.update(dict2)
        return x

    def test_errors(self):
        self.assertEqual(
            self.queue.get(),
            {})

        with self.assertRaises(ValueError):
            self.queue.add('BuiltIn', 'invalid')

        with self.assertRaises(KeyError):
            self.queue.set('NotHere')

    def test_queue(self):
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('BuiltIn', 'library')
        self.expected['BuiltIn'] = self._join_dict(
            self.status, self.lib)
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('BuiltIn', 'library')
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('some_resource.robot', 'resource')
        self.expected['some_resource.robot'] = self._join_dict(
            self.status, self.resource)
        self.assertEqual(
            self.queue.queue,
            self.expected)

        self.queue.add('Selenium2Library', 'library')
        self.expected['Selenium2Library'] = self._join_dict(
            self.status, self.lib)
        self.assertEqual(
            self.queue.queue,
            self.expected)

        data = self.queue.get()
        except_data = self.expected.items()[0]
        self.expected.popitem(last=False)
        except_data[1]['scanned'] = 'queued'
        self.expected['BuiltIn'] = except_data[1]
        self.assertEqual(data, except_data)
        self.assertEqual(self.queue.queue, self.expected)

        self.queue.add('BuiltIn', 'library')
        self.assertEqual(self.queue.queue, self.expected)

        self.queue.set('BuiltIn')
        except_data = self.expected.items()[-1]
        except_data[1]['scanned'] = True
        self.expected['BuiltIn'] = except_data[1]
        self.assertEqual(self.queue.queue, self.expected)
