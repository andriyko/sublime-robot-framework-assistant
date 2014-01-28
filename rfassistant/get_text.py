#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime

# Python imports
import re


def get_text_at_pos(line, col):
    """
    Gets text at current position defined with line and column values.
    """
    length = len(line)
    if length == 0:
        return None
        # between spaces
    if all([col >= length or line[col] == ' ' or line[col] == '\t',
            col == 0 or line[col-1] == ' ' or line[col-1] == '\t']):
        return None
        # first look back until we find 2 spaces in a row, or reach the beginning
    i = col - 1
    while i >= 0:
        if line[i] == '\t' or all([line[i - 1] == ' ' or line[i - 1] == '|', line[i] == ' ']):
            break
        i -= 1
    begin = i + 1
    # now look forward or until the end
    i = col  # previous included line[col]
    while i < length:
        if line[i] == '\t' or (line[i] == ' ' and len(line) > i and (line[i + 1] == ' ' or line[i + 1] == '|')):
            break
        i += 1
    end = i
    return line[begin:end]


def get_text_under_cursor(view):
    """
    Gets caret position and returns text at this position.
    """
    sel = view.sel()[0]
    line = re.compile('\r|\n').split(view.substr(view.line(sel)))[0]
    row, col = view.rowcol(sel.begin())
    return get_text_at_pos(line, col)


def select_item_and_do_action(view, results, action):
    """
    Executes action on selected item.
    """
    # map of actions and corresponding callbacks
    # callback builds results that are suitable for relevant action
    supported_actions = {
        'show_doc_in_browser': 'build_result_string_for_external_definitions',
        'show_doc_in_editor': 'build_result_string_for_doc_definitions',
        'goto_source': 'build_result_string_for_source_definitions'
    }
    if action not in supported_actions.keys():
        raise ValueError('\'%s\'. Must be one from: %s' % ', '.join(supported_actions.keys()))

    if len(results) == 1 and results[0].allow_unprompted_go_to():
        return getattr(results[0], action)(view)
    callback = supported_actions[action]

    # build unique results
    result_strings = []
    unique_results = []
    for index, kw in enumerate(results):
        res_string = tuple(getattr(kw, callback)())
        if res_string not in result_strings:
            result_strings.append(res_string)
            unique_results.append(results[index])

    # 'show_quick_panel' requires list() of lists, so convert it back
    result_strings[:] = [list(item) for item in result_strings]

    def on_done(index):
        if index == -1:
            text_under_cursor = get_text_under_cursor(view)
            message = 'No information available for: {0}'.format(text_under_cursor) \
                if text_under_cursor else 'No information available for text under cursor'
            return sublime.status_message(message)
        getattr(unique_results[index], action)(view)

    view.window().show_quick_panel(result_strings, on_done)
