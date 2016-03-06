import re
from json import load as json_load
try:
    from current_view import KW_COMPLETION
except:
    from ..current_view import KW_COMPLETION


class ReturnKeywordAndObject(object):
    """From line searches the keyword name and possible object

    Purpose of the library is to find and normalize the keyword
    name and object name. So that keyword documentation can be found
    database.
    """
    def __init__(self, current_view, rf_cell):
        self.index_data = None
        self.current_view = current_view
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
        BuiltIn.Comment or Comment. ``rf_cell`` is separeted based
        on the object names and keywords found from the
        current_view.json file. If object and/or keyword can not be
        found from the rf_cell, empty values are returned.
        """
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
                    if self.kw_equals_kw_candite(kw, keyword_canditate):
                        object_best_match = object_canditate
                        keyword_best_match = keyword_canditate
        return object_best_match, keyword_best_match

    def kw_equals_kw_candite(self, kw, kw_candite):
        """Returns True if kw == kw_canditate

        Spaces, under score are removed and
        strings are converted to lower before validation.
        """
        kw = kw.lower().replace(' ', '').replace('_', '')
        kw_candite = kw_candite.lower().replace(' ', '').replace('_', '')
        kw_candite = kw_candite.lstrip('.')
        return kw == kw_candite

    def _get_data(self):
        f = open(self.current_view)
        self.data = json_load(f)
        f.close()
