from collections import OrderedDict


class ParsingQueue(object):
    """This is queue for parsing test data and libraries"""
    def __init__(self):
        self.queue = OrderedDict({})

    def add(self, data):
        """Add item to the end of the queue.

        Does not add duplicates in the queue"""
        # {'library_name': {'scanned': False}}
        # {'resource_name': {'scanned': False}}
        if data not in self.queue:
            self.queue[data] = {'scanned': False}

    def get(self):
        """Get item from start of the queue"""
        try:
            return self.queue.popitem(last=False)
        except KeyError:
            return {}

    def update(self, data):
        """Update status to True"""
        self.queue[data] = {'scanned': True}
