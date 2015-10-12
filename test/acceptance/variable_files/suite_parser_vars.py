from os import path


def get_variables():
    root_dir = path.dirname(path.abspath(__file__))
    resource_dir = get_resource_path(root_dir)
    var = {}
    var['SIMPLE_RESOURCE'] = create_simple_resource(resource_dir)
    return var


def create_simple_resource(resource_dir):
    result = {}
    result['file_name'] = 'simple_resource.robot'
    result['file_path'] = path.join(resource_dir, 'simple_resource.robot')
    result['libraries'] = [{'library_name': 'Selenium2Library',
                            'library_alias': None}]
    result['resources'] = [path.join(resource_dir, 'simple_resrouce2.robot')]
    kws = {}
    # My Kw 1
    kw = {}
    kw['keyword_arguments'] = get_args(arg1='False', arg2='True')
    kw['documentation'] = 'Some documentation'
    kw['tags'] = ['some_tag', 'other_tag']
    kw['keyword_name'] = 'My Kw 1'

    kws['mykw1'] = kw
    # My Kw 2
    kw = {}
    kw['keyword_arguments'] = get_args(arg2='False', arg4=None)
    kw['documentation'] = 'Some documentation.\\nIn multi line'
    kw['tags'] = ['tag1']
    kw['keyword_name'] = 'My Kw 2'
    kws['mykw2'] = kw
    result['keywords'] = kws
    result['variables'] = ['${VAR1}']
    return result


def get_resource_path(root_dir):
    return path.normpath(
        path.join(
            root_dir,
            '..',
            '..',
            'resource',
            'test_data'
            )
        )


def get_args(**args):
    arg = []
    for k in args:
        if args[k] is not None:
            arg.append('${' + k + '}=${' + args[k] + '}')
        else:
            arg.append('${' + k + '}')
    return arg
