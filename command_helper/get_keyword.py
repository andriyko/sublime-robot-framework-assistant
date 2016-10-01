import re
from os import path
from sys import version_info
try:
    from get_documentation import GetKeywordDocumentation
    from db_json_settings import DBJsonSetting
    from noralize_cell import get_data_from_json
    from utils.util import kw_equals_kw_candite
except:
    from .get_documentation import GetKeywordDocumentation
    from ..setting.db_json_settings import DBJsonSetting
    from ..command_helper.noralize_cell import get_data_from_json
    from ..command_helper.utils.util import kw_equals_kw_candite


class GetKeyword(object):
    """Returns details to locate the file and keyword from the file

    Returns the real path to the file where the keyword is located.
    Also returns the regex patters which can be used to search the
    file from the documentation.
    """
    emebeded_re = '\\$\\{.+\\}'

    def __init__(self, table_dir, index_dir, open_tab, rf_extension):
        self.table_dir = table_dir
        self.index_dir = index_dir
        self.open_tab = open_tab
        self.rf_extension = rf_extension
        self.get_doc = GetKeywordDocumentation(
            table_dir=table_dir,
            index_dir=index_dir,
            open_tab=open_tab
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
        kw_details = self.get_doc.get_table_name_from_index(
            object_name,
            keyword
        )
        if not kw_details.table_name:
            return regex, file_path
        table_path = path.join(self.table_dir, kw_details.table_name)
        data = get_data_from_json(table_path)
        if DBJsonSetting.file_path in data:
            file_path_table = data[DBJsonSetting.file_path]
        else:
            file_path_table = None
        if self.rf_data(file_path_table):
            regex = self.get_regex_resource(kw_details.kw)
            file_path = file_path_table
            return regex, file_path
        else:
            return self.get_lib_keyword(
                table_path,
                kw_details.kw_object_name,
                kw_details.kw
            )

    def get_lib_keyword(self, table_path, object_name, keyword):
        regex = self.get_regex_library(keyword)
        file_path = self.get_lib_keyword_file(
            table_path,
            object_name,
            keyword
        )
        return regex, file_path

    def get_lib_keyword_file(self, table_path, object_name, keyword):
        """Returns file path from db where library keyword is defined"""
        data = get_data_from_json(table_path)
        table_keywords = data[DBJsonSetting.keywords]
        table_kw_object = data[DBJsonSetting.library_module]
        for table_kw_data in table_keywords:
            if kw_equals_kw_candite(keyword, table_kw_data):
                if not object_name or object_name == table_kw_object:
                    return table_keywords[table_kw_data][DBJsonSetting.keyword_file]

    def get_regex_library(self, keyword):
        """Returns the regex patters for library keywords"""
        if re.search(self.emebeded_re, keyword):
            return self._get_regex_lib_embedded(keyword)
        else:
            return self._get_regex_lib_no_embedded(keyword)

    def _get_regex_lib_embedded(self, keyword):
        """returns regex for lib keyword with embedded args"""
        regex_from_deco = r'(?i)(\@keyword.+name=[\'"]'
        words = self.split_kw_to_words(keyword)
        for word in words:
            if re.search(self.emebeded_re, word):
                regex_from_deco = '{0}{1}[_ ]?'.format(
                    regex_from_deco,
                    self.emebeded_re
                )
            else:
                regex_from_deco = '{0}{1}[_ ]?'.format(
                    regex_from_deco,
                    word.lower()
                )
        return '{0})'.format(regex_from_deco.rstrip('[_ ]?'))

    def _get_regex_lib_no_embedded(self, keyword):
        """returns regex for lib keyword with no embedded args"""
        words = self.split_kw_to_words(keyword)
        regex_from_func = '(?im)(def '
        regex_from_deco = r'(\@keyword.+name=[\'"]'
        for word in words:
            regex_from_func = '{0}{1}_?'.format(regex_from_func, word.lower())
            regex_from_deco = '{0}{1}[_ ]'.format(
                regex_from_deco, word.lower()
            )
        regex_from_func = regex_from_func.rstrip('_?')
        regex_from_deco = regex_from_deco.rstrip('[_ ]')
        return r'{0}\()|{1})'.format(regex_from_func, regex_from_deco)

    def get_regex_resource(self, keyword):
        """Returns the regex for user defined keywords"""
        words = self.split_kw_to_words(keyword)
        regex_patter = '(?im)^'
        for word in words:
            if re.search(self.emebeded_re, word):
                regex_patter = '{0}{1}[_ ]?'.format(
                    regex_patter, self.emebeded_re)
            else:
                regex_patter = '{0}{1}[_ ]?'.format(regex_patter, word.lower())
        regex_patter = regex_patter.rstrip('[_ ]?')
        regex_patter = '{0}$'.format(regex_patter)
        return regex_patter

    def split_kw_to_words(self, keyword):
        words = []
        # Like: LOG
        if keyword.isupper() and '_' not in keyword and ' ' not in keyword:
            words.append(keyword)
        # Like: RunKeyword
        elif '_' not in keyword and ' ' not in keyword:
            words = re.findall('[a-zA-Z0-9][^A-Z0-9]*', keyword)
        # The rest, like: Run Keyword or run keyword
        else:
            [words.extend(word.split('_')) for word in keyword.split(' ')]
        return words

    def rf_data(self, file_path):
        """Returns True if open tab is Robot Framework resource or suite"""
        if self.is_string(file_path):
            return file_path.endswith(self.rf_extension)
        else:
            return None

    def is_string(self, str_):
        if version_info.major > 2:
            status = isinstance(str_, str)
        else:
            status = isinstance(str_, basestring)
        return status
