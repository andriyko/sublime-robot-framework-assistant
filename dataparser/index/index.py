import logging
import re
import multiprocessing
import xml.etree.ElementTree as ET
from os import path, listdir
from json import load as json_load
from json import dump as json_dump
from collections import namedtuple
from parser_utils.file_formatter import rf_table_name, lib_table_name
from parser_utils.util import get_index_name
from queue.queue import ParsingQueue
from data_parser.data_parser import DataParser
from db_json_settings import DBJsonSetting
from queue.finder import finder

logging.basicConfig(
    format='%(levelname)s:%(asctime)s: %(message)s',
    level=logging.DEBUG)


def index_a_table(params):
    """Index a table found from db_path.
    `params` - Tuple of: db_dir, table_name and index_dir

    This is a wrapper function for multiprocessing.Pool
    to create index for tables in multiple processes.
    """
    name = multiprocessing.current_process().name
    logging.info('Starting name: %s', name)
    db_path, table_name, index_path, xml_libraries = params
    index = Index(db_path, index_path, xml_libraries)
    index.index_consturctor(table_name)


class Index(object):
    """Reads the database and returns index's of keywords and variables"""

    def __init__(self, db_path, index_path, xml_libraries=None):
        self.queue = ParsingQueue()
        self.data_parser = DataParser()
        self.index_path = index_path
        self.db_path = db_path
        self.xml_libraries = xml_libraries
        self.library_alias = []

    def index_consturctor(self, table):
        """Creates a single table index.

        `table` - name of the db table where index is created

        Will walk on all imported resources and libraries and
        adds all keyword and variables to the index file.
        """
        logging.info('Creating index for: {0}'.format(table))
        index_table_path = self.get_index_path(table)
        data = self.create_index_for_table(self.db_path, table)
        self.write_data(index_table_path, data)
        self.library_alias = []

    def write_data(self, index_table_path, data):
        f = open(index_table_path, 'w')
        json_dump(data, f)
        f.close()

    def create_index_for_table(self, db_path, table_name):
        """Creates index for a single table.

        Index contains all imported kw and variables
        """
        self.queue.clear_queue()
        self.queue.add(table_name, None, None)
        self.add_builtin_to_queue(db_path)
        if self.xml_libraries:
            self.add_xml_libraries(self.xml_libraries)
        keywords = []
        variables = []
        while True:
            item = self.get_item_from_queue()
            if not item:
                break
            t_name = item[0]
            kws, vars_ = self.create_index(
                db_path,
                t_name,
                table_name
            )
            if kws:
                keywords.extend(kws)
            if vars_:
                variables.extend(vars_)
        return {
            DBJsonSetting.keywords: keywords,
            DBJsonSetting.variables: variables
        }

    def create_index(self, db_path, t_name, table_name):
        """Returns single table data for indexing

        `db_path`- Where database tables are found
        `t_name` - From which table to read the data
        `table_name`- Name of the table where index is created for
        """
        variables = []
        keywords = []
        data = None
        try:
            data, read_status = self.read_table(path.join(db_path, t_name))
            variables, keywords = self.parse_table_data(data, t_name)
        except ValueError:
                read_status = 2
        if read_status == 1:
            logging.warning('Error finding: %s', path.join(db_path, t_name))
            logging.debug('When creating index for: %s', table_name)
        elif read_status == 2:
            logging.error('Unknow ValueError on %s', t_name)
            if data:
                logging.debug(data)
            else:
                logging.debug('Looks like read_table error')
        return keywords, variables

    def add_builtin_to_queue(self, db_path):
        for table in listdir(db_path):
            if table.lower().startswith('builtin'):
                self.queue.add(table, None, None)
                return

    def add_xml_libraries(self, path_to_xml):
        """Adds the found xml libraries to the queue"""
        for file_ in finder(path_to_xml, 'xml'):
            root = ET.parse(file_).getroot()
            if root.attrib['type'] == DBJsonSetting.library:
                self.queue.add(lib_table_name(root.attrib['name']), None, None)

    def parse_table_data(self, data, t_name):
        var = self.get_variables(data)
        kw, args = self.get_keywords(data)
        if kw:
            object_name = self.get_object_name(data)
            kw_index = self.get_kw_for_index(
                kw, args, t_name, object_name)
        else:
            kw_index = []
        self.add_imports_to_queue(self.get_imports(data))
        self.queue.set(t_name)
        return var, kw_index

    def add_imports_to_queue(self, imports):
        for import_ in imports:
            self.queue.add(import_, None, None)

    def get_item_from_queue(self):
        item = self.queue.get()
        if not item:
            return item
        elif not item[1]['scanned']:
            return item
        else:
            return {}

    def get_object_name(self, data):
        object_name = None
        if DBJsonSetting.library_module not in data:
            object_name = data[DBJsonSetting.file_name].split('.')[0]
        elif DBJsonSetting.library_module in data:
            object_name = data[DBJsonSetting.library_module]
        if not object_name:
            raise ValueError('Parsing error: {0}'.format(data))
        else:
            return object_name

    def get_imports(self, data):
        result = []
        if DBJsonSetting.libraries in data:
            result += self.get_library_imports(data)
        if DBJsonSetting.variable_files in data:
            for var in data[DBJsonSetting.variable_files]:
                result.append(rf_table_name(var.keys()[0]))
        if DBJsonSetting.resources in data:
            for resource in data[DBJsonSetting.resources]:
                result.append(rf_table_name(resource))
        return result

    def get_library_imports(self, data):
        l = []
        for lib in data[DBJsonSetting.libraries]:
            if lib[DBJsonSetting.library_path]:
                lib_import = lib[DBJsonSetting.library_path]
            else:
                lib_import = lib[DBJsonSetting.library_name]
            lib_args = lib[DBJsonSetting.library_arguments]
            lib_data = None
            try:
                lib_data = self.data_parser.parse_library(
                    lib_import,
                    lib_args
                )
            except ValueError:
                message = ('Unable to parse library "{0}"'
                           ', with args: "{1}"'.format(lib_import, lib_args))
                logging.error(message)
            if lib_data:
                table_name = lib_table_name(
                    lib_data[DBJsonSetting.library_module]
                )
                l.append(table_name)
                self.library_alias.append(
                    (table_name, lib[DBJsonSetting.library_alias])
                )
        return l

    def get_variables(self, data):
        result = []
        if DBJsonSetting.variables in data:
            for var in data[DBJsonSetting.variables]:
                result.append(var)
        return result

    def get_keywords(self, data):
        kw_list = []
        arg_list = []
        if DBJsonSetting.keywords in data:
            kws = data[DBJsonSetting.keywords]
            for kw in kws.iterkeys():
                kw_list.append(kws[kw][DBJsonSetting.keyword_name])
                kw_args = self.get_kw_arguments(
                    kws[kw][DBJsonSetting.keyword_arguments])
                arg_list.append(kw_args)
        return kw_list, arg_list

    def get_kw_arguments(self, kw_args):
        """Formats keyword arguments to suite completions"""
        pattern = re.compile('(?:[\@\$\&]\{)(.+)(?:\})')
        comletion_args = []
        for arg in kw_args:
            arg_name, arg_default = self.split_arg(arg)
            match = pattern.search(arg_name)
            if not match:
                comletion_args.append(arg_name)
            else:
                arg_text = match.group(1)
                if arg.startswith('$') and arg_default:
                    comletion_args.append(
                        '{}={}'.format(
                            arg_text, arg_default
                        )
                    )
                elif arg.startswith('$') and not arg_default:
                    comletion_args.append(arg_text)
                elif arg.startswith('@'):
                    comletion_args.append('*{0}'.format(arg_text))
                else:
                    comletion_args.append('**{0}'.format(arg_text))
        return comletion_args

    def split_arg(self, arg):
        arg_name = arg
        arg_default = None
        if '=' in arg:
            arg_name, arg_default = arg.split('=', 1)
        return arg_name, arg_default

    def get_kw_for_index(
            self, kw_list, argument_list, table_name, object_name):
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword argument object_name table_name object_alias')
        kw_index = []
        library_alias = self.get_library_alias(table_name)
        for kw, argument in zip(kw_list, argument_list):
            kw_index.append(
                KeywordRecord(
                    keyword=kw,
                    argument=argument,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=library_alias
                )
            )
        return kw_index

    def get_library_alias(self, table_name):
        for library_alias in self.library_alias:
            if library_alias[0] == table_name and library_alias[1]:
                return library_alias[1]

    def read_table(self, t_path):
        try:
            f = open(t_path)
            status = 0
        except IOError:
            logging.warning('Could not open table: %s', t_path)
            similar = self.find_similar_table(t_path)
            logging.info('Instead of %s using: %s', t_path, similar)
            f = open(similar)
            status = 1
        data = json_load(f)
        f.close()
        return data, status

    def find_similar_table(self, t_path):
        path_ = path.dirname(t_path)
        name = path.basename(t_path).split('-', 1)[0]
        similar_table = None
        if path.exists(path_):
            dir_list = listdir(path_)
        else:
            dir_list = []
        for f_name in dir_list:
            if f_name.startswith(name):
                similar_table = path.join(path_, f_name)
        if not similar_table:
            raise ValueError(
                'Could not locate similar table to: {0}'.format(t_path))
        return similar_table

    def get_index_path(self, table):
        return path.join(self.index_path, get_index_name(table))
