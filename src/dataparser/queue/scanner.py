import shutil
from os import path, makedirs
from robot.errors import DataError
from finder import finder
from dataparser.parser.TestDataParser import TestDataParser
from queue import ParsingQueue


class Scanner(object):
    """Class to perform initial scanning of robot data.

    Creates initial database of keywords and variables. The class should
    be used when files are changed without saving them from Sublime. Example
    when files are changed by version control, like with git pull command.

    The database is folder where robot data is saved as json files.
    """
    def __init__(self):
        self.queue = ParsingQueue()
        self.rf_data_type = [None, 'test_suite', 'resource']

    def scan(self, workspace, ext, db_path):
        """Scan and create the database

        ``workspace`` --root folder where robot data is scanned.
        ``ext`` --Extension for included files.
        ``db_path`` --Directory where files are saved"""
        if not path.exists(workspace):
            raise EnvironmentError(
                'Workspace does not exist: {0}'.format(str(workspace)))
        if not path.dirname(workspace):
            raise EnvironmentError(
                'Workspace must be folder: {0}'.format(str(workspace)))
        if not path.exists(db_path):
            makedirs(db_path)
        else:
            shutil.rmtree(db_path)
            makedirs(db_path)
        for f in finder(workspace, ext):
            self.queue.add(f, None)
        #while True:
        #    item = self.get_item()
        #    if not item:
        #        return
        #    else:
        #        self.add_to_queue(item)
        #        self.put_item_to_db(item)

    def get_item(self):
        item = self.queue.get()
        if not item:
            return item
        elif not item[1]['scanned']:
            return item
        else:
            return {}

    def add_to_queue(self, item):
        """Add resources and libraries to queue"""
        for lib in item['libraries']:
            self.queue.add(lib['library_name'], 'library')
        for var_file in item['variable_files']:
            self.queue.add(var_file[0], 'variable_file')
        for resource in item['resources']:
            self.queue.add(resource, 'resource')

    def put_item_to_db(self, item):
        """Creates the json file to self.db_path"""
        pass

    def parse_all(self, item):
        if item[1]['type'] in self.rf_data_type:
            return self.scan_rf_data(item[0])
        elif item[1]['type'] == 'library':
            return TestDataParser().parse_library(item[0])
        elif item[1]['type'] == 'variable':
            return TestDataParser().parse_variable_file(item[0])
        else:
            raise ValueError('{0} is not Robot Framework data'.format(
                item))

    def scan_rf_data(self, f):
        """Scans test suite or resoruce file"""
        try:
            return TestDataParser().parse_resource(f)
        except DataError:
            return TestDataParser().parse_suite(f)
