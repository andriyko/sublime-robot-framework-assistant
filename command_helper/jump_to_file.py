import os
import re

try:
    from parser_utils.file_formatter import lib_table_name
    from noralize_cell import get_data_from_json
except ImportError:
    from ..dataparser.parser_utils.file_formatter import lib_table_name
    from .noralize_cell import get_data_from_json


class JumpToFile(object):

    def is_import(self, line):
        re_string = '(?i)^(\|\s|)(library|Resource)(\s\s|\s\|)'
        if re.search(re_string, line):
            return True
        else:
            return False

    def get_import(self, line):
        re_string = '(?i)(resource\s+|library\s+)(\|\s+|)(\S+)'
        match = re.search(re_string, line)
        return match.groups()[2]

    def get_path_resource_path(self, imported_file, open_tab):
        open_tab_dirname = os.path.dirname(open_tab)
        return os.path.abspath(os.path.join(open_tab_dirname, imported_file))

    def get_library_path(self, imported_lib, open_tab, db_dir):
        lib_path = ''
        if imported_lib.endswith('.py'):
            lib_path = self.get_path_resource_path(
                imported_file=imported_lib, open_tab=open_tab
            )
        else:
            imported_lib_utf8 = imported_lib.encode('utf-8')
            file_name = lib_table_name(imported_lib_utf8)
            file_name = str(file_name)
            file_path = os.path.join(db_dir, file_name)
            data = get_data_from_json(file_path)
            keywords = data.get('keywords')
            first_kw = keywords[list(keywords.keys())[0]]
            lib_path = first_kw['keyword_file']
        return lib_path

    def get_import_path(self, import_, open_tab, db_dir):
        if import_.lower().endswith('.robot'):
            file_path = self.get_path_resource_path(
                imported_file=import_,
                open_tab=open_tab
            )
        else:
            file_path = self.get_library_path(
                imported_lib=import_,
                open_tab=open_tab,
                db_dir=db_dir
            )
        return file_path
