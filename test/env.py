from os import path
import sys

ROOT_DIR = path.dirname(path.abspath(__file__))
UNIT_TEST_DIR = path.join(ROOT_DIR, "unit")
ACCEPTANCE_TEST_DIR = path.join(ROOT_DIR, "acceptance")
LIB_DIR = path.join(ROOT_DIR, "lib")
RESOURCES_DIR = path.join(ROOT_DIR, "resources")
TEST_LIBS_DIR = path.join(RESOURCES_DIR, "testlibs")
RESULTS_DIR = path.join(ROOT_DIR, "results")
SRC_DIR = path.normpath(path.join(ROOT_DIR, "..", "src"))

sys.path.insert(0, SRC_DIR)
sys.path.append(LIB_DIR)
sys.path.append(UNIT_TEST_DIR)
