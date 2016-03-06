from json import load as json_load


def get_data_from_json(json_file):
    f = open(json_file)
    data = json_load(f)
    f.close()
    return data
