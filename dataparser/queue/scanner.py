import shutil
import logging
import json
from os import path, makedirs
from robot.errors import DataError
from finder import finder
from data_parser.data_parser import DataParser
from queue import ParsingQueue
from parser_utils.file_formatter import rf_table_name, lib_table_name
from parser_utils.util import normalise_path
from db_json_settings import DBJsonSetting

logging.basicConfig(
    format='%(levelname)s:%(asctime)s: %(message)s',
    level=logging.DEBUG)


class Scanner(object):
    """Class to perform initial scanning of robot data.

    Creates initial database of keywords and variables. The class should
    be used when files are changed without saving them from Sublime. Example
    when files are changed by version control, like with git pull command.

    The database is folder where robot data is saved as json files.
    """
    def __init__(self):
        self.queue = ParsingQueue()
        self.parser = DataParser()
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
            self.queue.add(normalise_path(f), None, None)
        while True:
            item = self.get_item()
            if not item:
                return
            else:
                logging.info('Creating table for: {0}'.format(item[0]))
                try:
                    data = self.parse_all(item)
                    self.add_to_queue(data)
                    self.put_item_to_db(data, db_path)
                except ValueError:
                    logging.warning('Error in: %s', item[0])
                finally:
                    self.queue.set(item[0])

    def get_item(self):
        item = self.queue.get()
        if not item:
            return item
        elif not item[1]['scanned']:
            return item
        else:
            return {}

    def add_to_queue(self, data):
        """Add resources and libraries to queue"""
        if DBJsonSetting.libraries in data:
            self.add_libraries_queue(data[DBJsonSetting.libraries])
        if DBJsonSetting.variable_files in data:
            self.add_var_files_queue(data[DBJsonSetting.variable_files])
        if DBJsonSetting.resources in data:
            self.add_resources_queue(data[DBJsonSetting.resources])

    def put_item_to_db(self, item, db_path):
        """Creates the json file to self.db_path"""
        if DBJsonSetting.library_module in item:
            f_name = lib_table_name(item[DBJsonSetting.library_module])
        elif DBJsonSetting.file_path in item:
            f_name = rf_table_name(item[DBJsonSetting.file_path])
        f = open(path.join(db_path, f_name), 'w')
        f.write(json.dumps(item, indent=4))
        f.close()

    def parse_all(self, item):
        data_type = item[1]['type']
        if data_type in self.rf_data_type:
            return self.scan_rf_data(item[0])
        elif data_type == DBJsonSetting.library:
            return self.parser.parse_library(item[0], item[1]['args'])
        elif data_type == 'variable_file':
            return self.parser.parse_variable_file(item[0], item[1]['args'])
        else:
            raise ValueError('{0} is not Robot Framework data'.format(
                item))

    def scan_rf_data(self, f):
        """Scans test suite or resoruce file"""
        self.parser.unregister_console_logger()
        try:
            return self.parser.parse_resource(f)
        except DataError:
            self.parser.close_logger()
            self.parser.register_console_logger()
            return self.parser.parse_suite(f)
        finally:
            self.parser.register_console_logger()

    def add_libraries_queue(self, libs):
        for lib in libs:
            if lib[DBJsonSetting.library_path]:
                lib_module = lib[DBJsonSetting.library_path]
            else:
                lib_module = lib[DBJsonSetting.library_name]
            self.queue.add(
                lib_module,
                DBJsonSetting.library,
                lib[DBJsonSetting.library_arguments]
                )

    def add_var_files_queue(self, var_files):
        for var_file in var_files:
            file_name = var_file.keys()[0]
            self.queue.add(
                file_name,
                'variable_file',
                var_file[file_name]['variable_file_arguments']
            )

    def add_resources_queue(self, resources):
        for resource in resources:
            self.queue.add(resource, 'resource', None)

    def add_builtin(self):
        self.queue.add('BuiltIn', DBJsonSetting.library, [])
