from os import path
import sys

ROOT_DIR = path.dirname(path.abspath(__file__))
UNIT_TEST_DIR = path.join(ROOT_DIR, "unit")
ACCEPTANCE_TEST_DIR = path.join(ROOT_DIR, "acceptance")
RESOURCES_DIR = path.join(ROOT_DIR, "resource")
TEST_DATA_DIR = path.join(RESOURCES_DIR, "test_data")
RESULTS_DIR = path.join(ROOT_DIR, "results")
SRC_DIR = path.normpath(path.join(ROOT_DIR, "..", 'dataparser'))
COMMAND_HELPER_DIR = path.normpath(path.join(ROOT_DIR, "..", 'command_helper'))
SETTING_DIR = path.normpath(path.join(ROOT_DIR, "..", 'setting'))

sys.path.insert(0, SRC_DIR)
sys.path.append(UNIT_TEST_DIR)
