import shutil
from os import path, makedirs, listdir
from json import load as json_load
from json import dump as json_dump
from collections import namedtuple
from collections import OrderedDict
from dataparser.queue.scanner import rf_table_name, lib_table_name
from dataparser.queue.queue import ParsingQueue


class Index(object):
    """Reads the database and returns index's of keywords and variables"""

    def __init__(self):
        self.queue = ParsingQueue()

    def index_all_tables(self, db_dir, index_path):
        """Index all tables found from db_dir"""
        if path.exists(index_path):
            shutil.rmtree(index_path)
        makedirs(index_path)
        for table in listdir(db_dir):
            index_name = 'index-{0}'.format(table)
            f = open(path.join(index_path, index_name), 'w')
            data = self.create_index_for_table(db_dir, table)
            json_dump(data, f)
            f.close()

    def create_index_for_table(self, db_dir, table_name):
        """Creates index for a single table.

        Index contains all imported kw and variables"""
        self.queue.queue = OrderedDict({})
        self.queue.add(table_name, None, None)
        keywords = []
        variables = []
        while True:
            item = self.get_item_from_queue()
            if not item:
                break
            t_name = item[0]
            data = self.read_table(path.join(db_dir, t_name))
            var = self.get_variables(data)
            if var:
                variables.extend(var)
            kw = self.get_keywords(data)
            if kw:
                object_name = self.get_object_name(data)
                kw_index = self.get_kw_for_index(
                    kw, t_name,
                    object_name)
                keywords.extend(kw_index)
            self.add_imports_to_queue(self.get_imports(data))
            self.queue.set(t_name)
        return {'keyword': keywords, 'variable': variables}

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
            for lib in data['libraries']:
                result.append(
                    lib_table_name(lib['library_name'])
                    )
        if 'variable_files' in data:
            for var in data['variable_files']:
                result.append(rf_table_name(var))
        if 'resources' in data:
            for resource in data['resources']:
                result.append(rf_table_name(resource))
        return result

    def get_variables(self, data):
        result = []
        if 'variables' in data:
            for var in data['variables']:
                result.append(var)
        return result

    def get_keywords(self, data):
        kw_list = []
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
            data = json_load(f)
        except:
            raise
        finally:
            f.close()
        return data
