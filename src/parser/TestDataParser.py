from robot import parsing
from robot.variables.filesetter import VariableFileSetter
from robot.variables.store import VariableStore
from robot.variables.variables import Variables
from os import path
from converter import white_space


class TestDataParser():
    """ This class is used to parse different tables in test data.

    Class will return the the test data as in json format.
    """
    # Public
    def __init__(self):
        self.file_path = None
        self.rf_variables = Variables()
        self.rf_var_storage = VariableStore(self.rf_variables)

    def parse_resource(self, file_path):
        self.file_path = file_path
        model = parsing.ResourceFile(file_path).populate()
        return self._parse_robot_data(file_path, model)

    def parse_suite(self, file_path):
        self.file_path = file_path
        model = parsing.TestCaseFile(source=file_path).populate()
        return self._parse_robot_data(file_path, model)

    def parse_variable_file(self, file_path, args):
        data = {}
        data['file_name'] = path.basename(file_path)
        data['file_path'] = path.normpath(file_path)
        self.file_path = file_path
        setter = VariableFileSetter(self.rf_var_storage)
        var_list = []
        for variable in setter.set(file_path, args):
            var_list.append(variable[0])
        data['variables'] = sorted(var_list)
        return data

    def parse_library(self, file_path):
        pass

    # Private
    def _parse_robot_data(self, file_path, model):
        data = {}
        data['file_name'] = path.basename(file_path)
        data['file_path'] = path.normpath(file_path)
        data['keywords'] = self._get_keywords(model)
        data['variables'] = self._get_global_variables(model)
        lib, res, v_files = self._get_imports(model)
        data['resources'] = res
        data['libraries'] = lib
        data['variable_files'] = v_files
        return data

    def _get_keywords(self, model):
        kw_data = {}
        for kw in model.keywords:
            tmp = {}
            tmp['keyword_arguments'] = kw.args.value
            tmp['documentation'] = kw.doc.value
            tmp['tags'] = kw.tags.value
            tmp['keyword_name'] = kw.name
            kw_data[white_space.strip_and_lower(kw.name)] = tmp
        return kw_data

    def _get_imports(self, model):
        lib = []
        res = []
        var_files = []
        for setting in model.setting_table.imports:
            if setting.type == 'Library':
                lib.append(self._format_library(setting))
            elif setting.type == 'Resource':
                res.append(self._format_resource(setting))
            elif setting.type == 'Variables':
                var_files.append(self._format_variable_file(setting))
        return lib, res, var_files

    def _format_library(self, setting):
        data = {}
        data['library_name'] = setting.name
        data['library_alias'] = setting.alias
        return data

    def _format_resource(self, setting):
        if path.isfile(setting.name):
            return setting.name
        else:
            c_dir = path.dirname(self.file_path)
            return path.normpath(path.join(c_dir, setting.name))

    def _format_variable_file(self, setting):
        data = []
        if path.isfile(setting.name):
            v_path = setting.name
        else:
            c_dir = path.dirname(self.file_path)
            v_path = path.normpath(path.join(c_dir, setting.name))
        data.append(v_path)
        data += setting.args
        return data

    def _get_global_variables(self, model):
        var_data = []
        for var in model.variable_table.variables:
            var_data.append(var.name)
        return var_data
