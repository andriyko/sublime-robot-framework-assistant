from collections import OrderedDict
from copy import deepcopy
from db_json_settings import DBJsonSetting


class ParsingQueue(object):
    """This is queue for parsing test data and libraries"""
    def __init__(self):
        self.queue = OrderedDict({})
        self.rf_types = [
            DBJsonSetting.library,
            'test_suite',
            'resource',
            None,
            'variable_file'
            ]

    def add(self, data, rf_type, arg):
        """Add item to the end of the queue.

        Does not add duplicates in the queue. ``rf_type``
        defines the type of the added item. Possible values are:
        `library`, `test_suite`, `resource` and None. rf_type=None is used
        when it is not know is the file type resource or a test suite.
        """
        if rf_type not in self.rf_types:
            raise ValueError('Invalid rf_type: {0}'.format(rf_type))
        if data not in self.queue:
            new = OrderedDict([(
                data,
                {'scanned': False, 'type': rf_type, 'args': arg})])
            old = self.queue
            self.queue = OrderedDict(list(new.items()) + list(old.items()))

    def get(self):
        """Get item from start of the queue"""
        try:
            data = self.queue.popitem(last=False)
            tmp = deepcopy(data)
            tmp[1]['scanned'] = 'queued'
            self.queue[tmp[0]] = tmp[1]
            return data
        except KeyError:
            return {}

    def set(self, data):
        """Set scanned to True and put item as last item in the queue"""
        status = self.queue[data]
        status['scanned'] = True
        self.queue[data] = status

    def force_set(self, data):
        """Adds items to the end of the queue with scanned == True"""
        status = {'scanned': True, 'type': None, 'args': None}
        if data in self.queue:
            del self.queue[data]
        self.queue[data] = status

    def clear_queue(self):
        """Clears all items in the queue"""
        self.queue = OrderedDict({})
