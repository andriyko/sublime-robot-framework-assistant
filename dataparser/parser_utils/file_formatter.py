from hashlib import md5
from os import path


def rf_table_name(f_path):
    md5sum = md5(f_path.encode('utf-8')).hexdigest()
    return '{realname}-{md5}.json'.format(
        realname=path.basename(f_path)[-100:],
        md5=md5sum
    )


def lib_table_name(library):
    return '{realname}-{md5}.json'.format(
        realname=library[-100:].decode('ascii'),
        md5=md5(library).hexdigest()
    )
