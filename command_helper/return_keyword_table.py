import re
from json import load as json_load


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

    def _get_data(self):
        f = open(self.current_view)
        self.data = json_load(f)
        f.close()
