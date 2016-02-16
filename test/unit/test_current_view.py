import unittest
import env
import shutil
import json
import hashlib
from os import path, makedirs, remove
from time import sleep
from index.index import Index
from queue.scanner import Scanner
from current_view import CurrentView


class TestIndexing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_dir = path.join(
            env.RESULTS_DIR,
            'db_dir'
        )
        cls.clean_dir(cls.db_dir)
        cls.index_dir = path.join(
            env.RESULTS_DIR,
            'index_dir'
        )
        cls.clean_dir(cls.index_dir)
        cls.workspace = path.join(
            env.TEST_DATA_DIR,
            'suite_tree'
        )
        scanner = Scanner()
        scanner.scan(
            cls.workspace,
            'robot',
            cls.db_dir)
        index = Index()
        index.index_all_tables(
            cls.db_dir,
            cls.index_dir
        )
        cls.test_a_index = path.join(
            env.RESOURCES_DIR,
            'index-test_a.robot-41883aa9e5af28925d37eba7d2313d57.json')

    def setUp(self):
        self.current_view = path.join(
            env.RESULTS_DIR,
            'current_view',
            'current_view.json'
        )
        self.open_tab = path.join(
            self.workspace,
            'test_a.robot'
        )
        self.other_tab = path.join(
            self.workspace,
            'test_b.robot')
        if not path.exists(path.dirname(self.current_view)):
            makedirs(path.dirname(self.current_view))
        elif path.exists(self.current_view):
            remove(self.current_view)
        self.cv = CurrentView()

    def test_view_same(self):
        view_db = path.dirname(self.current_view)
        self.assertEqual(
            self.cv.view_same(
                self.open_tab,
                view_db),
            False
        )
        self.make_current_view()
        self.assertEqual(
            self.cv.view_same(
                self.open_tab,
                view_db),
            True
        )
        self.assertEqual(
            self.cv.view_same(
                self.other_tab,
                view_db),
            False
        )

    def test_create_view(self):
        view_db = path.dirname(self.current_view)
        self.cv.create_view(self.open_tab, view_db, self.index_dir)
        f = open(self.current_view, 'r')
        data = json.load(f)
        f.close()
        expected = {}
        expected['variable'] = [
            "${TEST_A}",
            "${COMMON_VARIABLE_1}",
            "${COMMON_VARIABLE_2}",
            "${RESOURCE_A}"
        ]
        expected['kw_completion'] = self.completions()
        self.assertEqual(data['variable'], expected['variable'])
        self.assertEqual(data['kw_completion'], expected['kw_completion'])

    def test_view_in_db(self):
        ext = 'robot'
        self.assertEqual(
            self.cv.view_in_db(
                self.workspace,
                self.open_tab,
                self.index_dir,
                ext
            ), True)
        self.assertEqual(
            self.cv.view_in_db(
                self.workspace,
                self.other_tab,
                self.index_dir,
                ext
            ), True)
        not_in_workspace = path.join(
            env.TEST_DATA_DIR,
            'real_suite',
            'test',
            'real_suite.robot'
        )
        self.assertEqual(
            self.cv.view_in_db(
                self.workspace,
                not_in_workspace,
                self.index_dir,
                ext
            ), False)
        not_rf_file = path.join(
            self.workspace,
            'common_variables.py'
        )
        self.assertEqual(
            self.cv.view_in_db(
                self.workspace,
                not_rf_file,
                self.index_dir,
                ext
            ), False)
        not_found_file = path.join(
            self.workspace,
            'not_here.robot'
        )
        self.assertEqual(
            self.cv.view_in_db(
                self.workspace,
                not_found_file,
                self.index_dir,
                ext
            ), False)

    @classmethod
    def clean_dir(cls, directory):
        if path.exists(directory):
            while path.exists(directory):
                shutil.rmtree(directory)
                sleep(0.1)
        makedirs(directory)

    def make_current_view(self):
        data = {}
        data['view_md5'] = hashlib.md5(self.open_tab).hexdigest()
        data['file_name'] = path.basename(self.open_tab)
        f = open(self.current_view, 'w')
        json.dump(data, f)
        f.close()

    def completions(self):
        completions = []
        added_object_name = []
        f = open(self.test_a_index)
        data = json.load(f)
        f.close()
        for i in data['keyword']:
            kw = i[0].replace('_', ' ').title()
            object_name = i[1]
            completions.append([kw, object_name])
            if object_name not in added_object_name:
                completions.append([object_name, object_name])
                added_object_name.append(object_name)
        return completions
