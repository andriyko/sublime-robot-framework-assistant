import re


def get_line(view):
    """Returns line and column where cursor is

    ``view`` is sublime.View.
    """
    sel = view.sel()[0]
    line = view.substr(view.line(sel))  # gets the line text
    row, column = view.rowcol(sel.begin())  # gets the line number and column
    return line, column


def get_prefix(line, column):
    """Return prefix for vars and text right side of the cursor"""
    m = re.search('\S*$', line[:column])
    rside = line[column:]
    match = m.group(0)
    return {'match': match, 'rside': rside}


def get_object_from_line(line, prefix, column):
    """Returns the object name after the prefix

    ``line``   -- Text in the line where cursor is.
    ``prefix`` -- Prefix determined by sublime.
    ``column`` -- Index of the cursor in the line.
    """
    re_str = r'(?:\s)([^\s]+)(?:\.{0})$'.format(prefix)
    match = re.search(re_str, line[:column])
    if match:
        return match.group(1)
    else:
        return None
