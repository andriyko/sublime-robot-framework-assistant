from os import path
from json import load as json_load
from collections import namedtuple
from dataparser.queue.scanner import rf_table_name, lib_table_name


class Index(object):
    """Reads the database and returns index's of keywords and variables"""

    def __init__(self):
        self.index_queue = []

    def create_index(self, db_dir, f_name, index_dir):
        table_name = rf_table_name(f_name)
        data = self.read_table(path.join(db_dir, table_name))
        keywords = self.get_keywords(data)
        imports = self.get_imports(data)
        variables = self.get_variables(data)

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
