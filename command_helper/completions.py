import re
from json import load as json_load
try:
    from current_view import KW_COMPLETION
    from current_view import VARIABLE
except:
    from .current_view import KW_COMPLETION
    from .current_view import VARIABLE

VAR_RE_STRING = '[\$\@\&]\{?\w*$'


class VarMode(object):
    """Which contents mode is used for variables

    Describes how variable is found from the Sublime prefix
    """
    no_brackets = 1
    two_brackets = 2
    start_bracket = 3


def get_completion_list(view_index, prefix, text_cursor_rigt, rf_cell):
    if re.search(VAR_RE_STRING, prefix):
        return get_var_completion_list(view_index, prefix, text_cursor_rigt)
    else:
        return get_kw_completion_list(view_index, prefix, rf_cell)


def get_kw_re_string(prefix):
    prefix = str(prefix)
    re_string = '(?i)('
    qualifier = '.*'
    for index in prefix:
        re_string = '{re_string}{qualifier}{index}'.format(
            re_string=re_string, qualifier=qualifier, index=index)
    re_string = '{re_string}{close_re}'.format(
        re_string=re_string, close_re=')')
    return re_string


def get_kw_completion_list(view_index, prefix, rf_cell):
    pattern = re.compile(get_kw_re_string(prefix))
    match_keywords = []
    for keyword in get_keywords(view_index):
        kw = keyword[0]
        args = keyword[1]
        lib = keyword[2]
        if pattern.search(kw):
            kw_completion = create_kw_completion_item(kw, args, rf_cell, lib)
            match_keywords.append(kw_completion)
    return match_keywords


def get_var_re_string(prefix):
    prefix = str(prefix)
    ignore_case = '(?i)'
    if not re.search(VAR_RE_STRING, prefix):
        re_string = '{0}\\{1}'.format(ignore_case, prefix)
    else:
        re_string = ignore_case
        pattern = re.compile('[\$\@\&]')
        var_position = 0
        for index in prefix:
            if var_position == 0 and pattern.search(index):
                var_position = 1
            if var_position == 1:  # @ or $ & character
                re_string = '{0}\\{1}'.format(re_string, index)
                var_position = 2
            elif var_position == 2:  # { character
                re_string = '{0}\\{1}'.format(re_string, index)
                var_position = 3
            elif var_position == 3:  # rest of the variable
                re_string = '{0}.*{1}'.format(re_string, index)
    return re_string


def get_var_completion_list(view_index, prefix, text_cursor_rigt):
    pattern = re.compile(get_var_re_string(prefix))
    match_vars = []
    mode = get_var_mode(prefix, text_cursor_rigt)
    for var in get_variables(view_index):
        if pattern.search(var):
            match_vars.append(create_var_completion_item(var, mode))
    return match_vars


def get_var_mode(prefix, text_cursor_rigt):
    one_character = '[\@\$\&]'
    two_characters = '{0}\\{{'.format(one_character)
    if (re.search(two_characters, prefix) and
            text_cursor_rigt.startswith('}')):
        return VarMode.two_brackets
    elif re.search(two_characters, prefix) and not text_cursor_rigt:
        return VarMode.start_bracket
    elif re.search(one_character, prefix) and not text_cursor_rigt:
        return VarMode.no_brackets
    else:
        return VarMode.no_brackets


def create_kw_completion_item(kw, kw_args, rf_cell, source):
    trigger = '{trigger}\t{hint}'.format(trigger=kw, hint=source)
    if kw_args:
        completion = '{0}\n'.format(kw)
    else:
        completion = kw
    for arg in kw_args:
        completion = '{0}{1}{2}\n'.format(completion, '...' + rf_cell, arg)
    return (trigger, completion.rstrip('\n'))


def create_var_completion_item(var, mode):
    if mode == VarMode.no_brackets:
        return (var, '{0}'.format(var[1:]))
    elif mode == VarMode.two_brackets:
        return (var, '{0}'.format(var[2:-1]))
    elif mode == VarMode.start_bracket:
        return (var, '{0}'.format(var[2:]))


def _get_data(view_index):
    with open(view_index) as f:
        return json_load(f)


def get_keywords(view_index):
    return _get_data(view_index)[KW_COMPLETION]


def get_variables(view_index):
    return _get_data(view_index)[VARIABLE]
