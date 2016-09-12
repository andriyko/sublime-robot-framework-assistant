import shutil
import logging
import json
import os
import xml.etree.ElementTree as ET
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
    def __init__(self, xml_libraries=None):
        self.queue = ParsingQueue()
        self.parser = DataParser()
        self.rf_data_type = [None, 'test_suite', 'resource']
        self.xml_libraries = xml_libraries

    def scan(self, workspace, ext, db_path):
        """Scan and create the database
        ``workspace`` --root folder where robot data is scanned.
        ``ext`` --Extension for included files.
        ``db_path`` --Directory where files are saved"""
        if not os.path.exists(workspace):
            raise EnvironmentError(
                'Workspace does not exist: {0}'.format(str(workspace)))
        if not os.path.dirname(workspace):
            raise EnvironmentError(
                'Workspace must be folder: {0}'.format(str(workspace)))
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        else:
            shutil.rmtree(db_path)
            os.makedirs(db_path)
        self.add_builtin()
        if self.xml_libraries:
            self.add_xml_libraries(self.xml_libraries)
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

    def scan_single_file(self, file_path, db_path):
        """Scan a single file and create the database table for the file
        `file_path` -- Path to the file which is scanned.
        `db_path`   -- Directory where scan result is saved.
        """
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        logging.info('Creating table for: {0}'.format(file_path))
        item = (file_path, {'scanned': False, 'type': None, 'args': None})
        try:
            data = self.parse_all(item)
            self.put_item_to_db(data, db_path)
        except ValueError:
            logging.warning('Error in: %s', file_path)

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
        f = open(os.path.join(db_path, f_name), 'w')
        json.dump(item, f)
        f.close()

    def parse_all(self, item):
        data_type = item[1]['type']
        if data_type in self.rf_data_type:
            return self.scan_rf_data(item[0])
        elif data_type == DBJsonSetting.library:
            return self.parser.parse_library(item[0], item[1]['args'])
        elif data_type == DBJsonSetting.variable_file:
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

    def add_xml_libraries(self, path_to_xml):
        """Adds the found xml libraries to the queue"""
        for file_ in finder(path_to_xml, 'xml'):
            root = ET.parse(file_).getroot()
            if root.attrib['type'] == DBJsonSetting.library:
                self.queue.add(file_, DBJsonSetting.library, [])
