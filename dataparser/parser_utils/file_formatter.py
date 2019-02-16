import sys
from hashlib import md5
from os import path

PY2 = sys.version_info[0] < 3


def rf_table_name(f_path):
    md5sum = md5(f_path.encode('utf-8')).hexdigest()
    return '{realname}-{md5}.json'.format(
        realname=path.basename(f_path)[-100:],
        md5=md5sum
    )


def lib_table_name(library):
    if PY2:
        real_name = library[-100:].decode('ascii')
    else:
        real_name = library[-100:]
    if PY2:
        md5_hex = md5(library).hexdigest()
    else:
        md5_hex = md5(library.encode('utf-16')).hexdigest()
    return '{realname}-{md5}.json'.format(
        realname=real_name, md5=md5_hex)

