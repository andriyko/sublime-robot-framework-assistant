import unittest
import env
import os
import shutil
import json
from time import sleep
from collections import namedtuple
from queue.scanner import Scanner
from queue.scanner import rf_table_name, lib_table_name
from index.index import Index


class TestIndexing(unittest.TestCase):

    """The content of the db_fir was created with scanner by scanning the
    TEST_DATA_DIR/suite_tree folder. If scanner is changed, db_dir must
    be recreated."""

    @classmethod
    def setUpClass(cls):
        cls.db_dir = os.path.join(
            env.RESULTS_DIR,
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
        cls.xml_libs = os.path.join(
            env.RESOURCES_DIR,
            'library'
        )

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
        self.index = Index(self.db_dir, self.index_dir)

    def test_parse_table_data(self):
        t_name = os.path.join(
            env.RESOURCES_DIR,
            'BuiltIn-ca8f2e8d70641ce17b9b304086c19657.json'
        )
        self.index.queue.add(t_name, None, None)
        data, status = self.index.read_table(
            os.path.join(env.RESOURCES_DIR, t_name))
        var, kw_index = self.index.parse_table_data(data, t_name)
        self.assertTrue(u'${/}' in var)
        self.assertTrue('${OUTPUT_FILE}' in var)
        self.assertTrue('@{TEST_TAGS}' in var)

    def test_add_builtin(self):
        self.index.add_builtin_to_queue(self.db_dir)
        self.assertTrue(len(self.index.queue.queue) > 0)

    def test_read_table(self):
        data, read_status = self.index.read_table(
            os.path.join(
                self.db_dir,
                self.test_b_table_name))
        self.assertTrue(data['file_name'], 'test_b.robot')

    def test_get_keywords_resource(self):
        data = self.get_resource_b()
        expected_kw_list = [
            'Resource B Keyword 3 Many Args'
            'Embedding ${arg} To Keyword Name',
            'Resource B Keyword 2',
            'Resource B Keyword 1'
        ]
        expected_arg_list = [['kwb1'], []]
        kw_list, arg_list = self.index.get_keywords(data)
        self.assertEqual(kw_list.sort(), expected_kw_list.sort())
        self.assertEqual(arg_list.sort(), expected_arg_list.sort())

        data = self.get_test_a()
        expected_kw_list = ['Test A Keyword', 'Keyword']
        kw_list, arg_list = self.index.get_keywords(data)
        self.assertEqual(kw_list, expected_kw_list)
        self.assertEqual(arg_list, [[], []])

        data = self.get_s2l()
        parsed_kw, arg_list = self.index.get_keywords(data)
        self.assertTrue('Set Window Position' in parsed_kw)
        self.assertTrue('Get Cookies' in parsed_kw)
        self.assertTrue('Unselect Frame' in parsed_kw)
        self.assertTrue(['name'] in arg_list)
        l = ['driver_name', 'alias', 'kwargs', '**init_kwargs']
        self.assertTrue(l in arg_list)
        self.assertTrue(['*code'] in arg_list)

    def test_get_imports(self):
        data = self.get_resource_b()
        import_list = [self.process_table_name, self.lib_longer_100_characters]
        self.assertEqual(self.index.get_imports(data), import_list)

        data = self.get_test_a()
        import_list = [
            self.common_table_name,
            self.resource_a_table_name]
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
            'keyword argument object_name table_name object_alias')
        l, kw_list, arg_list, object_name, table_name = \
            self.get_resource_b_kw_index(KeywordRecord)
        self.assertEqual(
            self.index.get_kw_for_index(
                kw_list, arg_list, table_name, object_name), l)

        l, kw_list, arg_list, object_name, table_name = \
            self.get_test_a_kw_index(KeywordRecord)
        self.assertEqual(
            self.index.get_kw_for_index(
                kw_list, arg_list, table_name, object_name), l)

        l, kw_list, arg_list, object_name, table_name = self.get_s2l_kw_index(
            KeywordRecord)
        self.assertEqual(
            self.index.get_kw_for_index(
                kw_list, arg_list, table_name, object_name), l)

    def test_index_creation_test_a(self):
        table_name = self.test_a_table_name
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword argument object_name table_name object_alias')
        kw_list = []
        kw_list.extend(self.get_test_a_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_common_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_resource_a_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_s2l_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_os_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_builtin_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_LibNoClass_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_LongName_kw_index(KeywordRecord)[0])
        var_list = [
            u'${TEST_A}',
            u'${RESOURCE_A}',
            u'${COMMON_VARIABLE_1}',
            u'${COMMON_VARIABLE_2}'
        ]
        t_index = {
            'keywords': kw_list,
            'variables': var_list}
        r_index = self.index.create_index_for_table(self.db_dir, table_name)
        self.assertEqual(
            r_index['variables'].sort(), t_index['variables'].sort())
        self.assertEqual(len(r_index['keywords']), len(t_index['keywords']))
        self.assertEqual(
            r_index['keywords'].sort(),
            t_index['keywords'].sort()
        )

    def test_index_creation_test_b(self):
        table_name = self.test_b_table_name
        KeywordRecord = namedtuple(
            'KeywordRecord',
            'keyword argument object_name table_name object_alias')
        kw_list = []
        kw_list.extend(self.get_test_b_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_common_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_resource_b_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_s2l_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_process_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_builtin_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_LongName_kw_index(KeywordRecord)[0])
        kw_list.extend(self.get_OtherNameLib_kw_index(KeywordRecord)[0])
        var_list = [
            u'${TEST_B}',
            u'${RESOURCE_B}',
            u'${COMMON_VARIABLE_1}',
            u'${COMMON_VARIABLE_2}'
        ]
        t_index = {
            'keywords': kw_list,
            'variables': var_list}
        r_index = self.index.create_index_for_table(self.db_dir, table_name)
        self.assertEqual(
            r_index['variables'].sort(), t_index['variables'].sort())
        self.assertEqual(len(r_index['keywords']), len(t_index['keywords']))
        self.assertEqual(
            r_index['keywords'].sort(),
            t_index['keywords'].sort()
        )

    def test_index_consturctor(self):
        self.index.index_consturctor(self.resource_a_table_name)
        files = os.listdir(self.index_dir)
        self.assertEqual(len(files), 1)
        with open(os.path.join(self.index_dir, files[0])) as f:
            data = json.load(f)
        self.assertIn('variables', data)
        self.assertIn('keywords', data)
        self.assertFalse(
            any(kw[0] == 'Test A Keyword' for kw in data['keywords'])
        )
        self.assertTrue(
            any(kw[0] == 'Resource A Keyword 1' for kw in data['keywords'])
        )

    def test_get_kw_arguments(self):
        kw_args = [u'item', u'msg=None']
        result = self.index.get_kw_arguments(kw_args)
        expected = [u'item', u'msg']
        self.assertEqual(result, expected)
        kw_args = [u'name', u'*args']
        result = self.index.get_kw_arguments(kw_args)
        self.assertEqual(result, kw_args)
        kw_args = []
        result = self.index.get_kw_arguments(kw_args)
        self.assertEqual(result, kw_args)
        kw_args = [u'object=None', u'*args', u'**kwargs']
        result = self.index.get_kw_arguments(kw_args)
        expected = [u'object', u'*args', u'**kwargs']
        self.assertEqual(result, expected)
        kw_args = [u'${kwa1}', '@{list}', '&{kwargs}']
        result = self.index.get_kw_arguments(kw_args)
        expected = [u'kwa1', '*list', '**kwargs']
        self.assertEqual(result, expected)
        kw_args = ['${arg1}=${True}', '${arg2}=Text_here', '${arg3}=${False}']
        result = self.index.get_kw_arguments(kw_args)
        expected = ['arg1=${True}', 'arg2=Text_here', 'arg3=${False}']
        self.assertEqual(result, expected)

    def test_add_xml_libraries(self):
        self.assertEqual(len(self.index.queue.queue), 0)
        self.index.add_xml_libraries(self.xml_libs)
        self.assertEqual(len(self.index.queue.queue), 2)

    def test_index_with_xml_libraries(self):
        xml_libs = os.path.join(
            env.RESOURCES_DIR,
            'library'
        )
        db_dir_with_xml = os.path.join(
            env.RESULTS_DIR,
            'db_dir_with_xml')
        scanner = Scanner(xml_libs)
        scanner.scan(
            self.suite_dir,
            'robot',
            db_dir_with_xml
        )
        index = Index(db_dir_with_xml, self.index_dir, self.xml_libs)
        index.index_consturctor(self.resource_a_table_name)
        files = os.listdir(self.index_dir)
        self.assertEqual(len(files), 1)
        with open(os.path.join(self.index_dir, files[0])) as f:
            data = json.load(f)
        self.assertTrue(
            any(kw[2] == 'SwingLibrary' for kw in data['keywords'])
        )
        self.assertTrue(
            any(kw[0] == 'Add Table Cell Selection' for kw in data['keywords'])
        )
        self.assertTrue(
            any(kw[0] == 'Select From Popup Menu' for kw in data['keywords'])
        )

    def test_get_object_name(self):
        object_name = self.index.get_object_name(self.get_libnoclass())
        self.assertEqual(object_name, 'LibNoClass')
        object_name = self.index.get_object_name(self.get_resource_b())
        self.assertEqual(object_name, 'resource_b')
        object_name = self.index.get_object_name(self.get_os())
        self.assertEqual(object_name, 'OperatingSystem')
        object_name = self.index.get_object_name(self.get_s2l())
        self.assertEqual(object_name, 'Selenium2Library')

    def test_library_with_alias(self):
        data = self.index.create_index_for_table(self.db_dir,
                                                 self.common_table_name)
        for kw in data['keywords']:
            if 'Long Name Keyword' == kw.keyword:
                self.assertEqual(
                    kw.object_name,
                    'LibraryWithReallyTooLongName'
                )
                self.assertEqual(
                    kw.object_alias,
                    'LongName')

    @property
    def common_table_name_index(self):
        index = 'index-{0}'.format(self.common_table_name)
        return os.path.join(self.index_dir, index)

    @property
    def test_a_table_name_index(self):
        index = 'index-{0}'.format(self.test_a_table_name)
        return os.path.join(self.index_dir, index)

    @property
    def real_suite_table_name(self):
        return rf_table_name(
            os.path.normcase(
                os.path.join(
                    self.real_suite_dir,
                    'test',
                    'real_suite.robot'
                )
            )
        )

    @property
    def resource_b_table_name(self):
        return rf_table_name(
            os.path.normcase(os.path.join(self.suite_dir, 'resource_b.robot'))
        )

    @property
    def common_table_name(self):
        return rf_table_name(
            os.path.normcase(os.path.join(self.suite_dir, 'common.robot'))
        )

    @property
    def test_a_table_name(self):
        return rf_table_name(
            os.path.normcase(os.path.join(self.suite_dir, 'test_a.robot'))
        )

    @property
    def test_b_table_name(self):
        return rf_table_name(
            os.path.normcase(os.path.join(self.suite_dir, 'test_b.robot'))
        )

    @property
    def resource_a_table_name(self):
        return rf_table_name(os.path.normcase(
            os.path.join(self.suite_dir, 'resource_a.robot'))
        )

    @property
    def s2l_table_name(self):
        return lib_table_name('Selenium2Library')

    @property
    def os_table_name(self):
        return lib_table_name('OperatingSystem')

    @property
    def process_table_name(self):
        return lib_table_name('Process')

    @property
    def builtin_table_name(self):
        return lib_table_name('BuiltIn')

    @property
    def libnoclass_table_name(self):
        return lib_table_name('LibNoClass')

    @property
    def lib_longer_100_characters(self):
        return lib_table_name(
            'LibraryNameWhichIsLongerThan100CharactersButItSeems'
            'ThatItRequiresQuiteAlotLettersInTheFileNameAndIsNot'
            'GoodRealLifeExample'
        )

    @property
    def longname_table_name(self):
        return lib_table_name('LibraryWithReallyTooLongName')

    def get_resource_b(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.resource_b_table_name
            )
        )
        return json.load(f)

    def get_common(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.common_table_name
            )
        )
        return json.load(f)

    def get_test_a(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.test_a_table_name
            )
        )
        return json.load(f)

    def get_s2l(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.s2l_table_name
            )
        )
        return json.load(f)

    def get_os(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.os_table_name
            )
        )
        return json.load(f)

    def get_process(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.process_table_name
            )
        )
        return json.load(f)

    def getbuiltin(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.builtin_table_name
            )
        )
        return json.load(f)

    def get_libnoclass(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.libnoclass_table_name
            )
        )
        return json.load(f)

    def get_longname(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.longname_table_name
            )
        )
        return json.load(f)

    def get_other_name_lib(self):
        f = open(
            os.path.join(
                self.db_dir,
                self.lib_longer_100_characters
            )
        )
        return json.load(f)

    def get_s2l_kw_index(self, keywordrecord):
        s2l_data = self.get_s2l()
        kw_list = self.index.get_keywords(s2l_data)[0]
        arg_list = self.get_kw_args(s2l_data)
        object_name = 'Selenium2Library'
        table_name = self.s2l_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_os_kw_index(self, keywordrecord):
        os_data = self.get_os()
        kw_list = self.index.get_keywords(os_data)[0]
        arg_list = self.get_kw_args(os_data)
        object_name = 'OperatingSystem'
        table_name = self.os_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_process_kw_index(self, keywordrecord):
        data = self.get_process()
        kw_list = self.index.get_keywords(data)[0]
        arg_list = self.get_kw_args(data)
        object_name = 'Process'
        table_name = self.process_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_builtin_kw_index(self, keywordrecord):
        data = self.getbuiltin()
        kw_list = self.index.get_keywords(data)[0]
        arg_list = self.get_kw_args(data)
        object_name = 'BuiltIn'
        table_name = self.builtin_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_LibNoClass_kw_index(self, keywordrecord):
        data = self.get_libnoclass()
        kw_list = self.index.get_keywords(data)[0]
        arg_list = self.get_kw_args(data)
        object_name = 'LibNoClass'
        table_name = self.libnoclass_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_LongName_kw_index(self, keywordrecord):
        data = self.get_longname()
        kw_list = self.index.get_keywords(data)[0]
        arg_list = self.get_kw_args(data)
        object_name = 'LibraryWithReallyTooLongName'
        table_name = self.libnoclass_table_name
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias='LongName'
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_OtherNameLib_kw_index(self, keywordrecord):
        data = self.get_other_name_lib()
        kw_list = self.index.get_keywords(data)[0]
        arg_list = ['argument']
        object_name = (
            'LibraryNameWhichIsLongerThan100CharactersBut'
            'ItSeemsThatItRequiresQuiteAlotLettersInThe'
            'FileNameAndIsNotGoodRealLifeExample'
        )
        table_name = self.lib_longer_100_characters
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias='OtherNameLib'
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_test_a_kw_index(self, keywordrecord):
        kw_list = [u'Test A Keyword', u'Keyword']
        arg_list = [None, None]
        table_name = self.test_a_table_name
        object_name = u'test_a.robot'
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_test_b_kw_index(self, keywordrecord):
        kw_list = []
        table_name = self.test_b_table_name
        object_name = u'test_a.robot'
        l = []
        return l, kw_list, [None], object_name, table_name

    def get_resource_a_kw_index(self, keywordrecord):
        kw_list = [u'Resource A Keyword 1', u'resource A Keyword 2']
        arg_list = ['kwa1', None]
        table_name = self.resource_a_table_name
        object_name = u'resource_a.robot'
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_resource_b_kw_index(self, keywordrecord):
        kw_list = [
            u'Resource B Keyword 1',
            u'resource B Keyword 2',
            u'Embedding ${arg} To Keyword Name',
            u'Resource B Keyword 3 Many Args']
        arg_list = ['kwb1', None, 'arg', ['arg1', 'arg2', 'arg3']]
        table_name = self.resource_b_table_name
        object_name = u'resource_b.robot'
        l = []
        for kw, arg in zip(kw_list, arg_list):
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=arg,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, arg_list, object_name, table_name

    def get_common_kw_index(self, keywordrecord):
        kw_list = [
            u'Common Keyword 2',
            u'common Keyword 1',
            u'Really Long Keyword To Test With Jumping To Keyword Does Not Scroll The Visible Area To A Wrong Place Should There Be More Words'
        ]
        table_name = self.common_table_name
        object_name = u'common.robot'
        l = []
        for kw in kw_list:
            l.append(
                keywordrecord(
                    keyword=kw,
                    argument=None,
                    object_name=object_name,
                    table_name=table_name,
                    object_alias=None
                )
            )
        return l, kw_list, [None], object_name, table_name

    def get_kw_args(self, data):
        arg_list = []
        kws = data["keywords"]
        for i in kws.iterkeys():
            args = kws[i]['keyword_arguments']
            for arg in args:
                if '=' in arg:
                    arg_list.append(arg.split('=')[0])
                else:
                    arg_list.append(arg)
        return arg_list
