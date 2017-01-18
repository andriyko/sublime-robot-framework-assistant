import re
import difflib
from json import load as json_load
try:
    from db_json_settings import DBJsonSetting
    from utils.get_text import get_prefix
except:
    from ..setting.db_json_settings import DBJsonSetting
    from ..command_helper.utils.get_text import get_prefix


def check_prefix(line, column, prefix):
    data = get_prefix(line, column)
    cell = '{0}{1}'.format(data['match'], data['rside'])
    match = re.search(r'(?i)[\$\@\&]\{{{0}\}}'.format(prefix), cell)
    if match:
        new_prefix = match.group()
    else:
        possible_prefix = line[column - 2: column + 1]
        possible_macth = re.search(r'(?i)[\$\@\&]\{?\}?', possible_prefix)
        if possible_macth:
            new_prefix = possible_macth.group()
        else:
            new_prefix = prefix
    s = difflib.SequenceMatcher(None, data['match'], new_prefix)
    column = s.find_longest_match(0, len(data['match']), 0, len(new_prefix))[2]
    return new_prefix, column


def get_completion_list(view_index, prefix, column, object_name,
                        one_line, rf_cell):
    """Returns completion list for variables and keywords

    ``view_index`` -- Path to open tab index file in database.
    ``prefix`` -- Prefix from Sublime for the completion
    ``column`` -- Cursor position in prefix
    ``object_name`` -- Library or resource object name
    ``one_line`` -- How keyword arguments are formatted
    ``rf_cell`` -- RF_CELL value from .tmPreferences

    Entry point for getting Robot Framework completion in using
    on_query_completions API from Sublime Text 3."""
    if re.search(r'[\$\@\&]', prefix):
        return get_var_completion_list(view_index, prefix, column)
    else:
        return get_kw_completion_list(
            view_index=view_index,
            prefix=prefix,
            rf_cell=rf_cell,
            object_name=object_name,
            one_line=one_line
        )


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


def get_kw_completion_list(view_index, prefix, rf_cell,
                           object_name, one_line):
    pattern = re.compile(get_kw_re_string(prefix))
    match_keywords = []
    match_objects = []
    for keyword in get_keywords(view_index):
        kw = keyword[0]
        args = keyword[1]
        lib = keyword[2]
        lib_alias = keyword[4]
        if not object_name:
            if pattern.search(kw):
                kw = create_kw_completion_item(
                    kw, args, rf_cell, lib, one_line
                )
                match_keywords.append(kw)
        elif lib == object_name and lib != kw:
            if pattern.search(kw):
                kw = create_kw_completion_item(
                    kw, args, rf_cell, lib, one_line
                )
                match_keywords.append(kw)
        elif lib_alias == object_name and lib_alias != kw:
            if pattern.search(kw):
                kw = create_kw_completion_item(
                    kw, args, rf_cell, lib_alias, one_line
                )
                match_keywords.append(kw)
        if not object_name and lib_alias and pattern.search(lib_alias):
            if lib_alias not in match_objects:
                lib_comletion = create_kw_completion_item(
                    lib_alias, '.', '', lib_alias, True
                )
                match_objects.append(lib_alias)
                match_keywords.append(lib_comletion)
        elif not object_name and pattern.search(lib):
            if lib not in match_objects:
                lib_comletion = create_kw_completion_item(
                    lib, '.', '', lib, True
                )
                match_objects.append(lib)
                match_keywords.append(lib_comletion)
    with_name = add_with_name(prefix, object_name, rf_cell)
    if with_name:
        match_keywords.append(with_name)
    return match_keywords


def get_var_re_string(prefix):
    prefix = str(prefix)
    re_string = r'(?i)'
    prefix_len = len(prefix)
    re_string = r'{0}\{1}'.format(re_string, prefix[:1])
    if prefix_len == 1:  # Assumed: $
        re_string = r'{0}.*'.format(re_string)
    elif prefix_len == 2:  # Assumed: ${
        re_string = r'{0}\{{.*'.format(re_string)
    elif prefix_len == 3:
        re_string = r'{0}\{{.*\}}'.format(re_string)
    else:
        re_string = r'{0}\{{.*'.format(re_string)
        for char in prefix[2:-1]:
            re_string = r'{0}{1}.*'.format(re_string, char)
        re_string = r'{0}\}}'.format(re_string)
    return re_string


def get_var_completion_list(view_index, prefix, column):
    pattern = re.compile(get_var_re_string(prefix))
    match_vars = []
    mode = get_var_mode(prefix)
    for var in get_variables(view_index):
        if pattern.search(var):
            match_vars.append(create_var_completion_item(var, mode))
    return match_vars


def get_var_mode(prefix):
    """Returns False if { in prefix.

    ``prefix`` -- Prefix for the completion

    Variable completion can be done in two ways and completion
    depends on which way variable is written. Possible variable
    complations are: $ and ${}. In last cursor is between
    curly braces.
    """
    return False if '{' in prefix else True


def _replace(matchobj):
    return matchobj.group().replace('$', '\$')


def multiline_kw_completion_item(kw, kw_args, rf_cell):
    kw = re.sub(r'\$\{.*\}', _replace, kw)
    if kw_args:
        completion = '{0}\n'.format(kw)
    else:
        completion = kw
    for arg in kw_args:
        completion = '{0}{1}{2}\n'.format(completion, '...' + rf_cell, arg)
    return completion.rstrip('\n')


def oneline_kw_completion_item(kw, kw_args, rf_cell):
    completion = re.sub(r'\$\{.*\}', _replace, kw)
    for arg in kw_args:
        completion = '{0}{1}{2}'.format(completion, rf_cell, arg)
    return completion


def create_kw_completion_item(kw, kw_args, rf_cell, source, one_line):
    """Returns single item to the completions list

    `one_line` -- Are arguments returned in single or multi line format
    """
    trigger = '{trigger}\t{hint}'.format(trigger=kw, hint=source)
    if one_line:
        completion = oneline_kw_completion_item(kw, kw_args, rf_cell)
    else:
        completion = multiline_kw_completion_item(kw, kw_args, rf_cell)
    return (trigger, completion)


def create_var_completion_item(var, mode):
    if mode:
        return (var, '{0}'.format(var[1:]))
    else:
        return (var, '{0}'.format(var[2:-1]))


def _get_data(view_index):
    with open(view_index) as f:
        return json_load(f)


def get_keywords(view_index):
    return _get_data(view_index)[DBJsonSetting.keywords]


def get_variables(view_index):
    return _get_data(view_index)[DBJsonSetting.variables]


def add_with_name(prefix, object_name, rf_cell):
    with_name = 'WITH NAME'
    if not object_name:
        if with_name.startswith(prefix):
            return create_kw_completion_item(
                with_name, '', rf_cell, with_name, True
            )
