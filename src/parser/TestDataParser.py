from robot import parsing
from robot.libdocpkg.robotbuilder import LibraryDocBuilder
from os import path


class TestDataParser():
    """ This class is used to parse different tables in test data.

    Class will return the the test data as in json format.
    """
    # Public
    def parse_resource(self, file_path):
        model = parsing.ResourceFile(file_path).populate()
        data = {}
        data['file_name'] = path.basename(file_path)
        data['file_path'] = path.normpath(file_path)
        data['keywords'] = self._get_keywords(model)
        data['variables'] = self._get_global_variables(model)
        data['resources'] = self._get_imports(model, 'resource')
        data['libraries'] = self._get_imports(model, 'library')
        return data

    def parse_suite(self, file_path):
        pass

    def parse_variable_file(self, file_path):
        pass

    def parse_library(self, file_path):
        pass

    # Private

    def _get_keywords(self, model):
        kw_data = {}
        for kw in model.keywords:
            tmp = {}
            tmp['keyword_arguments'] = kw.args.value
            tmp['documentation'] = kw.doc.value
            tmp['tags'] = kw.tags.value
            tmp['keyword_variables'] = self._get_kw_variables(kw)
            kw_data[kw.name] = tmp
        return kw_data

    def _get_imports(self, model, setting_type):
        lib = []
        res = []
        for setting in model.setting_table.imports:
            if setting.type == 'Library':
                lib.append(self._format_library(setting))
            else:
                res.append(self._format_resource(setting))
        if setting_type.lower() is 'library':
            return lib
        else:
            return res

    def _format_library(self, setting):
        data = {}
        data['library_name'] = setting.name
        data['library_alias'] = setting.alias
        return data

    def _format_resource(self, setting):
        data = {}
        data['resource_name'] = setting.name
        return data

    def _get_global_variables(self, model):
        var_data = []
        for var in model.variable_table.variables:
            var_data.append(var.name)
        return var_data

    def _get_kw_variables(self, kw):
        data = {}
        assigned_variables = []
        keyword_arguments = []
        for step in kw.steps:
            assigned_variables.append(step.assign)
            keyword_arguments.append(step.args)
        data['assigned_variables'] = assigned_variables
        data['keyword_arguments'] = keyword_arguments
        return data

if __name__ == '__main__':
    f_path = 'D:\\workspace\\robotframework-dataparser\\test\\resource\\test_data\\simple_resource.robot'
    x = DataParser()
    tmp = x.parse_data(f_path)
    print json.loads(tmp)
    model = parsing.ResourceFile(f_path).populate()
    for kw in model.keywords:
        print kw.return_.value
        print kw.tags.value
        for s in kw.steps:
            print '\tassign: {0}'.format(s.assign)
            print '\tname: {0}'.format(s.name)
            print '\targs: {0}'.format(s.args)
    for kw in model.keyword_table.keywords:
        print kw.name

    """
    model = parsing.ResourceFile(f_path).populate()
    print 'Name: {0}'.format(model.name)
    print 'Kw settings:'
    for kw in model.keywords:
        print '\tName: {0}'.format(kw.name)
        print '\tArgs: {0}'.format(kw.args.value)
        print '\tDocs: {0}'.format(kw.doc.value)
    print 'Variables'
    for var in model.variable_table.variables:
        print '\tName: {0}'.format(var.name)
    print 'Settings'
    for setting in model.setting_table.imports:
        print setting.name
        print setting.args
        print setting.alias
        print setting.type

    print model.directory
    print base64.b16encode(path.join(model.directory, model.name))
    """
    # print 'Library Selenium2Library'
    # x = LibraryDocBuilder()
    # lib = x.build('Selenium2Library')
    # for kw in lib.keywords:
    #     print kw.name
    #     print kw.args
