import env
import os
import sys
import shutil
from robot import run


def acceptance_test(options):
    print options
    if len(options) == 0:
        _acceptance_all()
    else:
        if '-s' in options or '--suite':
            _acceptance_include(options[1:])
        else:
            print 'Only "-s" or "--suite" supported'
            _exit(255)


def _acceptance_all():
    run(env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR)


def _acceptance_include(options):
    run(env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR,
        suite=options)


def clean_results():
    print 'Clean: {0}'.format(env.RESULTS_DIR)
    shutil.rmtree(env.RESULTS_DIR)
    os.mkdir(env.RESULTS_DIR)


def unit_test():
    print 'TODO'


def _help():
    print 'Usage: python run_test.py [-s suite_name]'
    return 255


def _exit(rc):
    sys.exit(rc)

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        _exit(_help())
    clean_results()
    unit_test()
    acceptance_test(sys.argv[1:])
