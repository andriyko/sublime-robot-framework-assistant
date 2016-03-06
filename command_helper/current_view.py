import hashlib
from os import path, listdir, mkdir
from json import load as json_load
from json import dump as json_dump
try:
    from parser_utils.file_formatter import rf_table_name
    from parser_utils.util import normalise_path
    from db_json_settings import DBJsonSetting
except:
    from ..dataparser.parser_utils.file_formatter import rf_table_name
    from ..dataparser.parser_utils.util import normalise_path
    from ..setting.db_json_settings import DBJsonSetting

VIEW_FILE_NAME = 'current_view.json'
VIEW_MD5 = 'view_md5'
KW_COMPLETION = 'completion'
VIEW_NAME = 'view_name'


class CurrentView(object):

    def create_view(self, new_view, view_db, index_db):
        """Changes the content of database/view_db/current_view.json

        ``new_view`` -- Path to the open tab in sublime.
        ``view_db``  -- Path to folder where current_view.json is.
        ``index_db`` -- Path in index database folder.

        When user changes between different robot framework data
        tabs, this function changes the context of the
        database/view_db/current_view.json. The current_view.json.
        is used to provide the completions for the Sublime
        on_query_completions API call.
        """
        view_path = path.join(view_db, VIEW_FILE_NAME)
        new_view = normalise_path(new_view)
        index_table = 'index-{0}'.format(rf_table_name(new_view))
        index_table = path.join(index_db, index_table)
        index_data = self.get_data(index_table)
        data = {}
        data[DBJsonSetting.variable] = index_data[DBJsonSetting.variable]
        data[VIEW_NAME] = new_view
        data[VIEW_MD5] = hashlib.md5(new_view.encode('utf-8')).hexdigest()
        data[KW_COMPLETION] = self.get_keyword_completions(index_data)
        if not path.exists(path.dirname(view_path)):
            mkdir(path.dirname(view_path))
        f = open(view_path, 'w')
        json_dump(data, f, indent=4)
        f.close()

    def view_in_db(self, workspace, open_tab, index_db, extension):
        workspace = path.normcase(str(workspace))
        open_tab = path.normcase(str(open_tab))
        if open_tab.startswith(workspace):
            return self.is_rf_file(open_tab, extension, index_db)
        else:
            return False

    def is_rf_file(self, view_path, extension, index_db):
        if view_path.endswith(extension):
            return self.is_in_index(view_path, index_db)
        else:
            return False

    def is_in_index(self, view_path, index_db):
        view_path = path.normcase(view_path)
        index_table = 'index-{0:s}'.format(rf_table_name(view_path))
        try:
            files = listdir(index_db)
        except:
            return False
        if index_table in files:
            return True
        else:
            return False

    def get_keyword_completions(self, index_data):
        completions = []
        added_object_name = []
        for i in index_data[DBJsonSetting.keyword]:
            kw = i[0]
            args = i[1]
            object_name = i[2]
            completions.append([kw, args, object_name])
            if object_name not in added_object_name:
                completions.append([object_name, [], object_name])
                added_object_name.append(object_name)
        return completions

    def view_same(self, new_view, view_db):
        view_path = path.join(view_db, VIEW_FILE_NAME)
        if path.exists(view_path):
            new_view_md5 = hashlib.md5(new_view).hexdigest()
            data = self.get_data(view_path)
            if data[VIEW_MD5] == new_view_md5:
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
