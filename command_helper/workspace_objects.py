from os import listdir, path
try:
    from noralize_cell import get_data_from_json
    from db_json_settings import DBJsonSetting
except:
    from ..command_helper.noralize_cell import get_data_from_json
    from ..setting.db_json_settings import DBJsonSetting


class WorkSpaceObjects(object):

    """Searches the available resources, libraries or variable files
    from the database. The Purpose is to ease the resource, library
    and variable file imports.
    """
    def __init__(self, view_db):
        self.view_db = view_db

    def get_imports(self, import_type):
        """Returns the available objects based on the import_type

        `import_type`  -- Defines which type of imports should be returned.

        If import_type is resource, then all available resources found from
        the database are returned. If import_type is library, then all
        available libraries are returned from the database. If import_type
        is variable, then then all available variable files are returned
        from the database.
        """
        imports = []
        if import_type == DBJsonSetting.library:
            imports = self.get_libraries()
        elif import_type == DBJsonSetting.variable_file:
            imports = self.get_variables()
        elif import_type == DBJsonSetting.resource_file:
            imports = self.get_resources()
        else:
            raise ValueError('Invalid import_type: {0}'.format(import_type))
        return imports

    def get_libraries(self):
        libraries = []
        for file in listdir(self.view_db):
            data = get_data_from_json(path.join(self.view_db, file))
            if self.is_library(data):
                if 'BuiltIn' not in data[DBJsonSetting.library_module]:
                    libraries.append(self.get_library_import(data))
        return libraries

    def is_library(self, data):
        return True if DBJsonSetting.library_module in data else False

    def get_library_import(self, data):
        import_ = None
        if DBJsonSetting.file_path in data:
            import_ = [
                data[DBJsonSetting.library_module],
                data[DBJsonSetting.file_path]
            ]
        else:
            import_ = [
                data[DBJsonSetting.library_module],
                data[DBJsonSetting.library_module]
            ]
        return import_

    def get_resources(self):
        resources = []
        for file in listdir(self.view_db):
            data = get_data_from_json(path.join(self.view_db, file))
            if self.is_resource(data):
                resources.append(self.get_resource_or_variable_import(data))
        return resources

    def is_resource(self, data):
        return True if DBJsonSetting.variable_files in data else False

    def get_resource_or_variable_import(self, data):
        """Returns path to resource of variable file."""
        import_ = None
        if DBJsonSetting.file_path in data:
            import_ = [
                data[DBJsonSetting.file_name],
                data[DBJsonSetting.file_path]
            ]
        return import_

    def get_variables(self):
        variables = []
        for file in listdir(self.view_db):
            data = get_data_from_json(path.join(self.view_db, file))
            if self.is_variable_file(data):
                variables.append(self.get_resource_or_variable_import(data))
        return variables

    def is_variable_file(self, data):
        return True if DBJsonSetting.keywords not in data else False
