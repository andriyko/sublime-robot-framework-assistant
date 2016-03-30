def get_rf_table_separator(view):
    """Returns RF_CELL from Robot.tmPreferences

    ``view`` is sublime.View.
    """
    # mete_info returns [{'name': 'RF_CELL', 'value': '    '}]
    for dictionary in view.meta_info('shellVariables', 0):
        if dictionary['name'] == 'RF_CELL':
            return dictionary['value']
