import env
import os
import sys
import unittest
import shutil
from robot import run as robot_run


def acceptance_test(options):
    if not options:
        return _acceptance_all()
    else:
        if '-s' in options or '--suite' in options:
            return _acceptance_include(options[1:])
        else:
            print 'Only "-s" or "--suite" supported'
            _exit(255)


def _acceptance_all():
    return robot_run(
        env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR,
        loglevel='trace'
    )


def _acceptance_include(options):
    return robot_run(
        env.ACCEPTANCE_TEST_DIR,
        outputdir=env.RESULTS_DIR,
        suite=options,
        loglevel='trace'
    )


def clean_results():
    print 'Clean: {0}'.format(env.RESULTS_DIR)
    if os.path.exists(env.RESULTS_DIR):
        shutil.rmtree(env.RESULTS_DIR)
    os.mkdir(env.RESULTS_DIR)


def unit_test():
    print 'Running unit test'
    sys.path.insert(0, env.COMMAND_HELPER_DIR)
    sys.path.insert(0, env.SETTING_DIR)
    sys.path.insert(0, env.SRC_DIR)
    sys.path.append(env.UNIT_TEST_DIR)
    # suite = unittest.TestLoader().loadTestsFromName(
    #     'test_current_view.TestIndexing.test_create_view')
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
    u_result = unit_test()
    a_result = acceptance_test(sys.argv[1:])
    if u_result.errors or u_result.failures:
        print 'Unit tests failed'
        print 'errors: ', u_result.errors
        print 'failures: ', u_result.failures
        _exit(u_result.errors)
    elif a_result != 0:
        print 'Acceptance tests failed'
        _exit(a_result)
    else:
        print 'All passed'
        _exit(0)
