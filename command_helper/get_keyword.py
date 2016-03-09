import re
from os import path
try:
    from get_documentation import GetKeywordDocumentation
    from db_json_settings import DBJsonSetting
    from noralize_cell import get_data_from_json
except:
    from .get_documentation import GetKeywordDocumentation
    from ..setting.db_json_settings import DBJsonSetting
    from ..command_helper.noralize_cell import get_data_from_json


class GetKeyword(object):
    """Returns details to locate the file and keyword from the file

    Returns the real path to the file where the keyword is located.
    Also returns the regex patters which can be used to search the
    file from the documentation.
    """
    def __init__(self, table_dir, index_dir, open_tab, rf_extension):
        self.table_dir = table_dir
        self.index_dir = index_dir
        self.open_tab = open_tab
        self.rf_extension = rf_extension
        self.get_doc = GetKeywordDocumentation(
            table_dir=table_dir,
            index_dir=index_dir,
            open_tab=open_tab,
            rf_extension=rf_extension
        )

    def return_file_and_patter(self, object_name, keyword):
        """Returns regex and filename patter to find keyword from the source

        ``keyword``     -- Keyword documentation to search from database.
        ``object_name`` -- Library or resource object name.

        Searches the file path where the keyword is located and forms the
        regex patter which can be used to search the keyword from the file.
        Can be used to get the keyword from the robot data or from the
        Python libraries.
        """
        regex = None
        file_path = None
        table_name = self.get_doc.get_table_name_from_index(object_name,
                                                            keyword)
        if not table_name:
            return regex, file_path
        table_path = path.join(self.table_dir, table_name)
        file_path_table = get_data_from_json(
            table_path)[DBJsonSetting.file_path]
        if self.rf_data(file_path_table):
            regex = self.get_regex_resource(keyword)
            file_path = file_path_table
            return regex, file_path
        else:
            print('Library keyword not yet supported')
            return regex, file_path

    def get_regex_resource(self, keyword):
        """Returns the regex patters for user defined keywords"""
        # Like: LOG
        if keyword.isupper() and '_' not in keyword and ' ' not in keyword:
            words = []
            words.append(keyword)
        # Like: RunKeyword
        elif '_' not in keyword and ' ' not in keyword:
            words = re.findall('[a-zA-Z0-9][^A-Z0-9]*', keyword)
        # The rest, like: Run Keyword or run keyword
        else:
            words = []
            [words.extend(word.split('_')) for word in keyword.split(' ')]
        regex_patter = '(?im)^'
        for word in words:
            regex_patter = '{0}{1}[_ ]?'.format(regex_patter, word.lower())
        regex_patter = regex_patter.rstrip('[_ ]?')
        return '{0}$'.format(regex_patter)

    def rf_data(self, file_path):
        """Returns True if open tab is Robot Framework resource or suite"""
        return file_path.endswith(self.rf_extension)
