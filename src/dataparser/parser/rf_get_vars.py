from robot.libraries.BuiltIn import BuiltIn
from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))


def get_internal_variables():
    b = BuiltIn()
    rf_vars = [k for k in b.get_variables()]
    t_file = path.join(ROOT_DIR, 'rf_vars.py')
    f = open(t_file, 'w')
    f.write('RF_VARS = ' + str(rf_vars))
    f.close()
