import env
import os
import sys
import glob
import unittest
from robot import run


def acceptance_test(options):
    print options
    if len(options) == 0:
        _acceptance_all()
    else:
        if '-s' in options or '--suite' in options:
            _acceptance_include(options[1:])
        else:
            print 'Only "-s" or "--suite" supported'
            _exit(255)


def _acceptance_all():
    run(env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR,
        loglevel='trace')


def _acceptance_include(options):
    run(env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR,
        suite=options,
        loglevel='trace')


def clean_results():
    print 'Clean: {0}'.format(env.RESULTS_DIR)
    if os.path.exists(env.RESULTS_DIR):
        os.chdir(env.RESULTS_DIR)
        for f in glob.glob('*'):
            os.unlink(f)
    else:
        os.mkdir(env.RESULTS_DIR)


def unit_test():
    print 'Running unit test'
    sys.path.insert(0, env.SRC_DIR)
    suite = unittest.TestLoader().discover(
        start_dir=env.UNIT_TEST_DIR,
        pattern='test*.py')
    return unittest.TextTestRunner(verbosity=2).run(suite)


def _help():
    print 'Usage: python run_test.py [-s suite_name]'
    return 255


def _exit(rc):
    sys.exit(rc)

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        _exit(_help())
    clean_results()
    result = unit_test()
    if result.errors == 0:
        print 'Unit test passed'
    acceptance_test(sys.argv[1:])
