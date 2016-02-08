import shutil
import logging
from os import path, makedirs, listdir
from json import load as json_load
from json import dump as json_dump
from collections import namedtuple
from queue.scanner import rf_table_name, lib_table_name
from queue.queue import ParsingQueue

logging.basicConfig(
    format='%(levelname)s:%(asctime)s: %(message)s',
    level=logging.DEBUG)


class Index(object):
    """Reads the database and returns index's of keywords and variables"""

    def __init__(self):
        self.queue = ParsingQueue()

    def index_all_tables(self, db_path, index_path):
        """Index all tables found from db_path"""
        if path.exists(index_path):
            shutil.rmtree(index_path)
        makedirs(index_path)
        for table in listdir(db_path):
            index_name = 'index-{0}'.format(table)
            f = open(path.join(index_path, index_name), 'w')
            data = self.create_index_for_table(db_path, table)
            json_dump(data, f, indent=4)
            f.close()

    def create_index_for_table(self, db_path, table_name):
        """Creates index for a single table.

        Index contains all imported kw and variables"""
        self.queue.clear_queue()
        self.queue.add(table_name, None, None)
        self.add_builtin_to_queue(db_path)
        keywords = []
        variables = []

        def internal_logger():
            logging.warning('Error finding: %s', path.join(db_path, t_name))
            logging.debug('When creating index for: %s', table_name)

        while True:
            item = self.get_item_from_queue()
            if not item:
                break
            t_name = item[0]
            try:
                data, read_status = self.read_table(path.join(db_path, t_name))
                var, kw_index = self.parse_table_data(
                    data, t_name)
                keywords.extend(kw_index)
                variables.extend(var)
            except ValueError:
                read_status = False
            if not read_status:
                internal_logger()
        return {'keyword': keywords, 'variable': variables}

    def add_builtin_to_queue(self, db_path):
        for table in listdir(db_path):
            if table.lower().startswith('builtin'):
                self.queue.add(table, None, None)
                return

    def parse_table_data(self, data, t_name):
        var = self.get_variables(data)
        kw = self.get_keywords(data)
        if kw:
            object_name = self.get_object_name(data)
            kw_index = self.get_kw_for_index(
                kw, t_name,
                object_name)
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
        if 'file_name' in data:
            return data['file_name']
        elif 'library_module' in data:
            return data['library_module']
        else:
            raise ValueError('Parsing error: {0}'.format(data))

    def get_imports(self, data):
        result = []
        if 'libraries' in data:
            result += self.get_library_imports(data)
        if 'variable_files' in data:
            for var in data['variable_files']:
                result.append(rf_table_name(var.keys()[0]))
        if 'resources' in data:
            for resource in data['resources']:
                result.append(rf_table_name(resource))
        return result

    def get_library_imports(self, data):
        l = []
        for lib in data['libraries']:
            if lib['library_path']:
                l.append(lib_table_name(lib['library_path']))
            else:
                l.append(lib_table_name(lib['library_name']))
        return l

    def get_variables(self, data):
        result = []
        if 'variables' in data:
            for var in data['variables']:
                result.append(var)
        return result

    def get_keywords(self, data):
        kw_list = []
        if 'keywords' in data:
            for kw in data['keywords'].iterkeys():
                kw_list.append(kw)
        return kw_list

    def get_kw_for_index(self, kw_list, table_name, object_name):
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword object_name table_name')
        l = []
        for kw in kw_list:
            l.append(
                KeywordRecord(
                    keyword=kw,
                    object_name=object_name,
                    table_name=table_name
                )
            )
        return l

    def read_table(self, t_path):
        try:
            f = open(t_path)
            status = True
        except IOError:
            logging.warning('Could not open table: %s', t_path)
            similar = self.find_similar_table(t_path)
            logging.info('Instead of %s using: %s', t_path, similar)
            f = open(similar)
            status = False
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
