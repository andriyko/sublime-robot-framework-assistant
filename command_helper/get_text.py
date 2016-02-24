import re


def get_line(view):
    """Returns line and column where cursor is

    ``view`` is sublime.View.
    """
    sel = view.sel()[0]
    line = view.substr(view.line(sel))  # prints Line text
    row, column = view.rowcol(sel.begin())  # Prints line number and column
    print(line, column)
    return line, column


def get_prefix(line, column):
    m = re.search('\S*$', column[:line])
    return m.group()
