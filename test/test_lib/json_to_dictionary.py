import json
from os import path


class JsonParser():

    def parse_json_from_file(self, path_to_file):
        """Example doc for testing"""
        with open(path.normpath(path_to_file)) as f:
            data = ''.join(f.readlines())
        f.close()
        return json.loads(data)

    def parse_json(self, json_data):
        return json.loads(json_data)

    def compare_dicts(self, dict1, dict2):
        if cmp(dict1, dict2):
            return True
        else:
            raise ValueError('{0} != {1}'.format(dict1, dict2))
