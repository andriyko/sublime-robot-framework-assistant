from json import load as json_load


def get_data_from_json(json_file):
    f = open(json_file)
    data = json_load(f)
    f.close()
    return data


def kw_equals_kw_candite(kw, kw_candite):
        """Returns True if kw == kw_canditate

        Spaces, under score are removed and
        strings are converted to lower before validation.
        """
        kw = kw.lower().replace(' ', '').replace('_', '')
        kw_candite = kw_candite.lower().replace(' ', '').replace('_', '')
        kw_candite = kw_candite.lstrip('.')
        return kw == kw_candite
