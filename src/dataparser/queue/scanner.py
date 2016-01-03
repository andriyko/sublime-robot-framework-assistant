import shutil
from os import path, makedirs
from hashlib import md5
import json
from robot.errors import DataError
from finder import finder
from dataparser.parser.TestDataParser import TestDataParser
from queue import ParsingQueue

LIBRARIES = 'libraries'
LIBRARY = 'library'


class Scanner(object):
    """Class to perform initial scanning of robot data.

    Creates initial database of keywords and variables. The class should
    be used when files are changed without saving them from Sublime. Example
    when files are changed by version control, like with git pull command.

    The database is folder where robot data is saved as json files.
    """
    def __init__(self):
        self.queue = ParsingQueue()
        self.parser = TestDataParser()
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
        self.add_builtin()
        for f in finder(workspace, ext):
            self.queue.add(f, None)
        while True:
            item = self.get_item()
            if not item:
                return
            else:
                data = self.parse_all(item)
                self.add_to_queue(data)
                self.put_item_to_db(data, db_path)

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
        if LIBRARIES in item:
            self.add_libraries_queue(item[LIBRARIES])
        if 'variable_files' in item:
            self.add_var_files_queue(item['variable_files'])
        if 'resources' in item:
            self.add_resources_queue(item['resources'])

    def put_item_to_db(self, item, db_path):
        """Creates the json file to self.db_path"""
        if 'file_path' in item:
            f_name = '{realname}-{md5}.json'.format(
                realname=path.basename(item['file_path']),
                md5=md5(item['file_path']).hexdigest()
                )
        elif 'library_module' in item:
            f_name = '{realname}-{md5}.json'.format(
                realname=item['library_module'],
                md5=md5(item['library_module']).hexdigest()
                )
        f = open(path.join(db_path, f_name), 'w')
        f.write(json.dumps(item, indent=4))
        f.close()

    def parse_all(self, item):
        if item[1]['type'] in self.rf_data_type:
            return self.scan_rf_data(item[0])
        elif item[1]['type'] == LIBRARY:
            return self.parser.parse_library(item[0])
        elif item[1]['type'] == 'variable':
            return self.parser.parse_variable_file(item[0])
        else:
            raise ValueError('{0} is not Robot Framework data'.format(
                item))

    def scan_rf_data(self, f):
        """Scans test suite or resoruce file"""
        self.parser.unregister_console_logger()
        try:
            return self.parser.parse_resource(f)
        except DataError:
            return self.parser.parse_suite(f)
        finally:
            self.parser.register_console_logger()

    def add_libraries_queue(self, libs):
        for lib in libs:
            self.queue.add(lib['library_name'], LIBRARY)

    def add_var_files_queue(self, var_files):
        for var_file in var_files:
            self.queue.add(var_file[0], 'variable_file')

    def add_resources_queue(self, resources):
        for resource in resources:
            self.queue.add(resource, 'resource')

    def add_builtin(self):
        self.queue.add('BuiltIn', LIBRARY)
