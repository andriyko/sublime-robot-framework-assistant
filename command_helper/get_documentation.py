import collections
from os import path
try:
    from parser_utils.file_formatter import rf_table_name
    from parser_utils.util import get_index_name, normalise_path
    from noralize_cell import get_data_from_json
    from db_json_settings import DBJsonSetting
    from utils.util import kw_equals_kw_candite
except:
    from ..dataparser.parser_utils.file_formatter import rf_table_name
    from ..dataparser.parser_utils.util import get_index_name, normalise_path
    from ..command_helper.noralize_cell import get_data_from_json
    from ..setting.db_json_settings import DBJsonSetting
    from ..command_helper.utils.util import kw_equals_kw_candite


class GetKeywordDocumentation(object):
    """Returns the keyword documentation from the database file"""
    def __init__(self, table_dir, index_dir, open_tab):
        self.table_dir = table_dir
        self.index_dir = index_dir
        self.open_tab = open_tab

    def return_documentation(self, object_name, keyword):
        """Returns the keyword documentation from the database.

        ``object_name`` -- Library or resource object name.
        ``keyword``     -- Keyword documentation to search from database.

        Searches the keyword documentation from the database and
        returns the keyword documentation if match is found.
        ``object_name`` can be used to separate keywords
        between the libraries that contains keyword with same name.

        Always the first match is returned but using the ``object_name``
        should guarantee that correct documentation is retrieved from
        the database.
        """
        documentation = None
        # table_name, kw_canditate, kw_object_name
        kw_details = self.get_table_name_from_index(
            object_name,
            keyword
        )
        if kw_details.table_name:
            table_path = path.join(self.table_dir, kw_details.table_name)
            documentation = self.get_keyword_documentation(
                table_path,
                kw_details.kw_object_name,
                kw_details.kw
            )
        return documentation

    def get_table_name_from_index(self, object_name, keyword):
        """Returns the keyword table name from the index table

        ``keyword``     -- Keyword documentation to search from database.
        ``object_name`` -- Library or resource object name.
        """
        return_kw = None
        return_table_name = None
        kw_object_name = None
        KwDetails = collections.namedtuple(
            'KwDetails',
            [
                'table_name',
                'kw',
                'kw_object_name'
            ]
        )
        open_tab = normalise_path(self.open_tab)
        index_name = get_index_name(rf_table_name(open_tab))
        index_data = get_data_from_json(
            path.join(self.index_dir, index_name)
        )
        for keyword_ in index_data[DBJsonSetting.keywords]:
            kw_canditate = keyword_[0]
            kw_object_name_alias = keyword_[4]
            kw_table_name = keyword_[3]
            kw_object_name = keyword_[2]
            if (object_name and
                    object_name == kw_object_name_alias or
                    object_name == kw_object_name):
                # Test kw if object names are equal
                if kw_equals_kw_candite(keyword, kw_canditate):
                    return_kw = kw_canditate
                    return_table_name = kw_table_name
                    break
            elif not object_name:
                if kw_equals_kw_candite(keyword, kw_canditate):
                    return_kw = kw_canditate
                    return_table_name = kw_table_name
                    break
        return KwDetails(
            table_name=return_table_name,
            kw=return_kw,
            kw_object_name=kw_object_name
        )

    def get_keyword_documentation(self, table_path, object_name, keyword):
        """Returns the keyword documentation from the table

        ``table_name``  -- Filename where the documentation is searched.
        ``keyword``     -- Keyword documentation to search from database.
        ``object_name`` -- Library or resource object name.

        """
        keywords = get_data_from_json(table_path)[DBJsonSetting.keywords]
        for keyword_ in keywords:
            if kw_equals_kw_candite(keyword, keyword_):
                return keywords[keyword_][DBJsonSetting.documentation]
