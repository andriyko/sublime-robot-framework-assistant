from hashlib import md5
from os import path


def rf_table_name(f_path):
    return '{realname}-{md5}.json'.format(
                realname=path.basename(f_path),
                md5=md5(f_path).hexdigest()
            )


def lib_table_name(library):
    if path.isfile(library):
        module = path.basename(library)
    else:
        module = library
    return '{realname}-{md5}.json'.format(
                realname=module,
                md5=md5(library).hexdigest()
            )
