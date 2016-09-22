import re
from json import load as json_load


def get_data_from_json(json_file):
    f = open(json_file)
    data = json_load(f)
    f.close()
    return data


def _keyword_with_embedded_arg(kw, kw_candite):
    kw = kw.lower().replace(' ', '').replace('_', '')
    kw_candite = kw_candite.lower().replace(' ', '').replace('_', '')
    kw_re = re.sub(r'(?i)(\$\{[\w ]*\})', r'(?i)(\S+)', kw_candite)
    return re.search(kw_re, kw)


def _keyword_no_embedded_arg(kw, kw_candite):
    kw = kw.lower().replace(' ', '').replace('_', '')
    kw_candite = kw_candite.lower().replace(' ', '').replace('_', '')
    kw_candite = kw_candite.lstrip('.')
    return kw == kw_candite


def kw_equals_kw_candite(kw, kw_candite):
        """Returns True if kw == kw_canditate

        Spaces, under score are removed and
        strings are converted to lower before validation.

        Also support keyword conditate with emedded args
        """
        if '$' in kw_candite:
            return _keyword_with_embedded_arg(kw, kw_candite)
        else:
            return _keyword_no_embedded_arg(kw, kw_candite)
