import re
import collections
try:
    from utils.util import get_data_from_json, kw_equals_kw_candite
    from db_json_settings import DBJsonSetting
except:
    from .utils.util import get_data_from_json, kw_equals_kw_candite
    from ..setting.db_json_settings import DBJsonSetting


class ReturnKeywordAndObject(object):
    """From line searches the keyword name and possible object

    Purpose of the library is to find and normalize the keyword
    name and object name. So that keyword documentation can be found
    database.
    """
    def __init__(self, current_index, rf_cell):
        # Path to index file for the currently
        # open tab in sublime text
        self.current_index = current_index
        self.rf_cell = rf_cell

    def normalize(self, line, column):
        """Returns the keyword and object from the line.

        ``line`` -- Full line text where cursor is.
        ``column`` -- Location of the cursor
        """
        keyword = None
        object_name = None
        rf_cell = self.get_rf_cell(line, column)
        if '.' not in rf_cell:
            keyword = rf_cell
        else:
            object_name, keyword = self.separate_keyword_from_object(rf_cell)
        return keyword, object_name

    def get_rf_cell(self, line, column):
        """Returns the cell from line where cursor is"""
        line_to_column = line[:column]
        line_from_column = line[column:]
        rf_cell = None
        to_column = re.search('(\S+ ?)+$', line_to_column)
        from_column = re.search('^( ?\S+ ?)+', line_from_column)
        if to_column and from_column:
            rf_cell = '{0}{1}'.format(
                to_column.group(),
                from_column.group().rstrip())
        elif not to_column and from_column:
            rf_cell = from_column.group()
        elif to_column and not from_column:
            rf_cell = to_column.group()
        return rf_cell

    def separate_keyword_from_object(self, rf_cell):
        """Separates keyword from the object.

        ``rf_cell`` -- cell where the cursor is.

        ``rf_cell`` must be a valid valid keyword. Example
        BuiltIn.Comment or Comment. ``rf_cell`` is separated based
        on the object names and keywords found from the
        index file. If object and/or keyword can not be
        found from the rf_cell, empty values are returned.
        """
        self._get_data()
        keywords = self.data[DBJsonSetting.keywords]
        object_best_match = ''
        keyword_best_match = ''
        for kw_detail in keywords:
            object_name = kw_detail[2]
            object_alias = kw_detail[4]
            kw_canditate = kw_detail[0]
            if rf_cell.startswith(object_name):
                match_found = self._separate_worker(
                    object_best_match,
                    object_name,
                    rf_cell,
                    kw_canditate
                )
            elif object_alias and rf_cell.startswith(object_alias):
                match_found = self._separate_worker(
                    object_best_match,
                    object_alias,
                    rf_cell,
                    kw_canditate
                )
            else:
                MatchFound = self.get_MatchFound()
                match_found = MatchFound(object=None, keyword=None)
            if match_found.keyword:
                object_best_match = match_found.object
                keyword_best_match = match_found.keyword
        return object_best_match, keyword_best_match

    def _separate_worker(self, object_best_match, object_canditate,
                         rf_cell, kw_canditate):
        MatchFound = self.get_MatchFound()
        object_ = ''
        keyword = ''
        if len(object_best_match) <= len(object_canditate):
            object_re = object_canditate.replace('.', '\\.')
            object_re = '(?:{0}\\.)(.+)'.format(object_re)
            match = re.search(object_re, rf_cell)
            if match:
                keyword_from_line = match.group(1)
            else:
                keyword_from_line = ''
            if kw_equals_kw_candite(keyword_from_line, kw_canditate):
                object_ = object_canditate
                keyword = keyword_from_line
        return MatchFound(object=object_, keyword=keyword)

    def get_MatchFound(self):
        MatchFound = collections.namedtuple(
            'MatchFound',
            [
                'object',
                'keyword'
            ]
        )
        return MatchFound

    def _get_data(self):
        self.data = get_data_from_json(self.current_index)
