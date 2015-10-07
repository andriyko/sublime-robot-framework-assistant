import env
import os
import sys
import glob
from robot import run


def acceptance_test(options):
    print options
    if len(options) == 0:
        _acceptance_all()
    else:
        if '-s' not in options or '--suite' not in options:
            print 'Only "-s" or "--suite" supported'
            _exit(255)
        else:
            _acceptance_include(options[1:])


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
