import re
try:
    from utils.util import get_data_from_json, kw_equals_kw_candite
except:
    from .utils.util import get_data_from_json, kw_equals_kw_candite


KW_COMPLETION = 'completion'


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
        if not rf_cell:
            pass
        elif '.' not in rf_cell:
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
        current_view.json file. If object and/or keyword can not be
        found from the rf_cell, empty values are returned.
        """
        self._get_data()
        completions = self.data[KW_COMPLETION]
        object_best_match = ''
        keyword_best_match = ''
        for kw_completion in completions:
            object_name = kw_completion[2]
            kw = kw_completion[0]
            if rf_cell.startswith(object_name):
                if len(object_best_match) <= len(object_name):
                    object_canditate = object_name
                    object_re = object_canditate.replace('.', '\\.')
                    object_re = '(?:{0}\\.)(.+)'.format(object_re)
                    match = re.search(object_re, rf_cell)
                    if match:
                        keyword_canditate = match.group(1)
                    else:
                        keyword_canditate = ''
                    if kw_equals_kw_candite(kw, keyword_canditate):
                        object_best_match = object_canditate
                        keyword_best_match = keyword_canditate
        return object_best_match, keyword_best_match

    def _get_data(self):
        self.data = get_data_from_json(self.current_view)
