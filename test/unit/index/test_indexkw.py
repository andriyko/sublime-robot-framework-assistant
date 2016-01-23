import unittest
import env
import os
import shutil
import json
from time import sleep
from collections import namedtuple
from dataparser.queue.scanner import Scanner
from dataparser.index.index import Index


class TestIndexing(unittest.TestCase):

    """The content of the db_fir was created with scanner by scanning the
    TEST_DATA_DIR/suite_tree folder. If scanner is changed, db_dir must
    be recreated."""

    @classmethod
    def setUpClass(cls):
        cls.db_dir = os.path.join(
            env.RESOURCES_DIR,
            'db_dir'
        )
        cls.suite_dir = os.path.join(
            env.TEST_DATA_DIR,
            'suite_tree'
        )
        scanner = Scanner()
        scanner.scan(
            cls.suite_dir,
            'robot',
            cls.db_dir)

    def setUp(self):
        self.index_dir = os.path.join(
            env.RESULTS_DIR,
            'index_dir',
        )
        if os.path.exists(self.index_dir):
            while os.path.exists(self.index_dir):
                shutil.rmtree(self.index_dir)
                sleep(0.1)
        os.makedirs(self.index_dir)
        self.index = Index()

    def test_read_table(self):
        data = self.index.read_table(
            os.path.join(
                self.db_dir,
                'test_b.robot-779d241623971b05b6c1fa507e4f1ab5.json'))
        self.assertTrue(data['file_name'], 'test_b.robot')

    def test_get_keywords_resource(self):
        data = self.get_resource_b()
        kw_list = ['resource_b_keyword_2', 'resource_b_keyword_1']
        self.assertEqual(self.index.get_keywords(data), kw_list)

        data = self.get_test_a()
        kw_list = ['test_a_keyword']
        self.assertEqual(self.index.get_keywords(data), kw_list)

        data = self.get_s2l()
        parsed_kw = self.index.get_keywords(data)
        self.assertTrue('set_window_position' in parsed_kw)
        self.assertTrue('get_cookies' in parsed_kw)
        self.assertTrue('unselect_frame' in parsed_kw)

    def test_get_imports(self):
        data = self.get_resource_b()
        import_list = ['Process-b6ec7abeb6ae29cc35a4b47475e12afe.json']
        self.assertEqual(self.index.get_imports(data), import_list)

        data = self.get_test_a()
        import_list = [
            'common.robot-c7d61b0da98ae8ac905b9596256934f2.json',
            'resource_a.robot-a8aeadbbe3564ef58fc8119b0cd766ec.json']
        self.assertEqual(
            self.index.get_imports(data).sort(), import_list.sort())

        data = self.get_s2l()
        self.assertEqual(self.index.get_imports(data), [])

    def test_get_variables(self):
        data = self.get_resource_b()
        var = ['${RESOURCE_B}']
        self.assertEqual(self.index.get_variables(data), var)

        data = self.get_test_a()
        var = ['${TEST_A}']
        self.assertEqual(
            self.index.get_variables(data).sort(), var.sort())

        data = self.get_s2l()
        self.assertEqual(self.index.get_variables(data), [])

        data = self.get_common()
        self.assertEqual(self.index.get_variables(data), [])

    def test_get_kw_for_index(self):
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword object_name table_name')
        kw_list = ['resource_b_keyword_2', 'resource_b_keyword_1']
        table_name = 'resource_b.robot-bc289af1f3ddcc4187b4a9785e075694.json'
        object_name = 'resource_b.robot'
        l = []
        for kw in kw_list:
            l.append(
                KeywordRecord(
                    keyword=kw,
                    object_name=object_name,
                    table_name=table_name
                )
            )
        self.assertEqual(
            self.index.get_kw_for_index(kw_list, table_name, object_name), l)

        l, kw_list, object_name, table_name = self.get_test_a_kw_index(
            KeywordRecord)
        self.assertEqual(
            self.index.get_kw_for_index(kw_list, table_name, object_name), l)

        l, kw_list, object_name, table_name = self.get_s2l_kw_index(
            KeywordRecord)
        self.assertEqual(
            self.index.get_kw_for_index(kw_list, table_name, object_name), l)

    def test_index_creation_test_a(self):
        table_name = 'test_a.robot-1852a118490abd2b0024027f490d5654.json'
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword object_name table_name')
        kw_list = []
        kw_list.extend(self.get_test_a_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_common_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_resource_a_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_s2l_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_os_kw_index(KeywordRecord)[0])
        var_list = [u'${TEST_A}', u'${RESOURCE_A}']
        t_index = {
            'keyword': kw_list,
            'variable': var_list}
        r_index = self.index.create_index_for_table(
                self.db_dir, table_name, self.index_dir)
        self.assertEqual(r_index['variable'], t_index['variable'])
        self.assertEqual(len(r_index['keyword']), len(t_index['keyword']))
        self.assertEqual(r_index['keyword'].sort(), t_index['keyword'].sort())

    def test_index_creation_test_b(self):
        table_name = 'test_b.robot-779d241623971b05b6c1fa507e4f1ab5.json'
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword object_name table_name')
        kw_list = []
        kw_list.extend(self.get_test_b_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_common_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_resource_b_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_s2l_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_process_kw_index(KeywordRecord)[0])
        var_list = [u'${TEST_B}', u'${RESOURCE_B}']
        t_index = {
            'keyword': kw_list,
            'variable': var_list}
        r_index = self.index.create_index_for_table(
                self.db_dir, table_name, self.index_dir)
        self.assertEqual(r_index['variable'], t_index['variable'])
        self.assertEqual(len(r_index['keyword']), len(t_index['keyword']))
        self.assertEqual(r_index['keyword'].sort(), t_index['keyword'].sort())

    def test_index_all_db(self):
        raise ValueError('Not done')

    def get_resource_b(self):
        f = open(os.path.join(
                self.db_dir,
                'resource_b.robot-bc289af1f3ddcc4187b4a9785e075694.json'
            )
        )
        return json.load(f)

    def get_common(self):
        f = open(os.path.join(
                self.db_dir,
                'common.robot-c7d61b0da98ae8ac905b9596256934f2.json'
            )
        )
        return json.load(f)

    def get_test_a(self):
        f = open(os.path.join(
                self.db_dir,
                'test_a.robot-1852a118490abd2b0024027f490d5654.json'
            )
        )
        return json.load(f)

    def get_s2l(self):
        f = open(os.path.join(
                self.db_dir,
                'Selenium2Library-ac72a5ed5dae4edc06e58114b7c0ce92.json'
            )
        )
        return json.load(f)

    def get_os(self):
        f = open(os.path.join(
                self.db_dir,
                'OperatingSystem-3f475567566b93c16c76ae4f3daaca1a.json'
            )
        )
        return json.load(f)

    def get_process(self):
        f = open(os.path.join(
                self.db_dir,
                'Process-b6ec7abeb6ae29cc35a4b47475e12afe.json'
            )
        )
        return json.load(f)

    def get_s2l_kw_index(self, keywordrecord):
        s2l_data = self.get_s2l()
        kw_list = self.index.get_keywords(s2l_data)
        object_name = 'Selenium2Library'
        table_name = 'Selenium2Library-ac72a5ed5dae4edc06e58114b7c0ce92.json'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name

    def get_os_kw_index(self, keywordrecord):
        os_data = self.get_os()
        kw_list = self.index.get_keywords(os_data)
        object_name = 'OperatingSystem'
        table_name = 'OperatingSystem-3f475567566b93c16c76ae4f3daaca1a.json'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name

    def get_process_kw_index(self, keywordrecord):
        process_data = self.get_process()
        kw_list = self.index.get_keywords(process_data)
        object_name = 'Process'
        table_name = 'Process-b6ec7abeb6ae29cc35a4b47475e12afe.json'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name

    def get_test_a_kw_index(self, keywordrecord):
        kw_list = [u'test_a_keyword']
        table_name = 'test_a.robot-1852a118490abd2b0024027f490d5654.json'
        object_name = u'test_a.robot'
        l = [keywordrecord(
            keyword=kw_list[0],
            object_name=object_name,
            table_name=table_name)]
        return l, kw_list, object_name, table_name

    def get_test_b_kw_index(self, keywordrecord):
        kw_list = []
        table_name = 'test_b.robot-779d241623971b05b6c1fa507e4f1ab5.json'
        object_name = u'test_a.robot'
        l = []
        return l, kw_list, object_name, table_name

    def get_resource_a_kw_index(self, keywordrecord):
        kw_list = [u'resource_a_keyword_1', u'resource_a_keyword_2']
        table_name = 'resource_a.robot-a8aeadbbe3564ef58fc8119b0cd766ec.json'
        object_name = u'resource_a.robot'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name

    def get_resource_b_kw_index(self, keywordrecord):
        kw_list = [u'resource_b_keyword_1', u'resource_b_keyword_2']
        table_name = 'resource_b.robot-bc289af1f3ddcc4187b4a9785e075694.json'
        object_name = u'resource_b.robot'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name

    def get_common_kw_index(self, keywordrecord):
        kw_list = [u'common_keyword_2', u'common_keyword_1']
        table_name = 'common.robot-c7d61b0da98ae8ac905b9596256934f2.json'
        object_name = u'common.robot'
        l = []
        for kw in kw_list:
            l.append(keywordrecord(
                keyword=kw, object_name=object_name, table_name=table_name))
        return l, kw_list, object_name, table_name
