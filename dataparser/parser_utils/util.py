from os import path


def normalise_path(f_path):
    dirname = path.abspath(path.dirname(f_path))
    basename = path.basename(f_path)
    dirname = path.normpath(path.normcase(dirname))
    return path.join(dirname, basename)
