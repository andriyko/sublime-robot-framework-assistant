from os import path
import hashlib
from json import load as json_load
from json import dump as json_dump
from queue.scanner import rf_table_name

VIEW_FILE_NAME = 'current_view.json'
VIEW_MD5 = 'view_md5'
KW_COMPLETION = 'kw_completion'
VIEW_NAME = 'view_name'
VARIABLE = 'variable'


class CurrentView(object):

    def __init__(self):
        self.data = None

    def create_view(self, new_view, view_db, index_db):
        view_path = path.join(view_db, VIEW_FILE_NAME)
        new_view = self.normalise_path(new_view)
        index_table = 'index-{0}'.format(rf_table_name(new_view))
        index_table = path.join(index_db, index_table)
        index_data = self.get_data(index_table)
        data = {}
        data[VARIABLE] = index_data['variable']
        data[VIEW_NAME] = new_view
        data[VIEW_MD5] = hashlib.md5(new_view).hexdigest()
        data[KW_COMPLETION] = self.get_keyword_completions(index_data)
        f = open(view_path, 'w')
        json_dump(data, f)
        f.close()

    def get_keyword_completions(self, index_data):
        completions = []
        added_object_name = []
        for i in index_data['keyword']:
            kw = i[0].replace('_', ' ').title()
            object_name = i[1]
            completions.append([kw, object_name])
            if object_name not in added_object_name:
                completions.append([object_name, object_name])
                added_object_name.append(object_name)
        return completions

    def view_same(self, new_view, view_db):
        view_path = path.join(view_db, VIEW_FILE_NAME)
        if path.exists(view_path):
            new_view_md5 = hashlib.md5(new_view).hexdigest()
            self.data = self.get_data(view_path)
            if self.data[VIEW_MD5] == new_view_md5:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def get_data(view_path):
        f = open(view_path, 'r')
        data = json_load(f)
        f.close()
        return data

    @staticmethod
    def normalise_path(f_path):
        dirname = path.abspath(path.dirname(f_path))
        basename = path.basename(f_path)
        dirname = path.normpath(path.normcase(dirname))
        return path.join(dirname, basename)
