import argparse
import sys
import shutil
import multiprocessing
from os import path, listdir, makedirs

ROOT_DIR = path.dirname(path.abspath(__file__))
SETTING_DIR = path.join(ROOT_DIR, '..', 'setting')
sys.path.append(SETTING_DIR)

from index.index import index_a_table
from index.index import Index


def index_all(db_path, index_path, module_search_path, libs_in_xml):
    for path_ in module_search_path:
        sys.path.append(path_)
    tables = listdir(db_path)
    params = []
    for table in tables:
        params.append((db_path, table, index_path, libs_in_xml))
    if path.exists(index_path):
        shutil.rmtree(index_path)
    makedirs(index_path)
    pool = multiprocessing.Pool()
    pool.map(index_a_table, params)


def index_single(db_path, db_table, index_path, module_search_path,
                 libs_in_xml):
    for path_ in module_search_path:
        sys.path.append(path_)
    if not path.exists(index_path):
        makedirs(index_path)
    index = Index(db_path=db_path, index_path=index_path,
                  xml_libraries=libs_in_xml)
    index.index_consturctor(table=db_table)

if __name__ == '__main__':
    c_parser = argparse.ArgumentParser(
        description='Indexing Scanner results')
    c_parser.add_argument(
        'mode',
        choices=['all', 'single'],
        help='Index mode: all or single'
    )
    c_parser.add_argument(
        '--db_path',
        required=True,
        help='Folder where Scanner result is read'
    )
    c_parser.add_argument(
        '--db_table',
        help='File name, in the db_path folder, where index is created'
    )
    c_parser.add_argument(
        '--index_path',
        required=True,
        help='Folder where index result is saved'
    )
    c_parser.add_argument(
        '--module_search_path',
        nargs='*',
        help='List of paths where libraries are searched when indexing')
    c_parser.add_argument(
        '--path_to_lib_in_xml',
        help='Path to libraries in XML format')
    args = c_parser.parse_args()
    module_search_path = []
    if args.module_search_path:
        module_search_path = args.module_search_path
    if args.mode == 'all':
        index_all(
            args.db_path,
            args.index_path,
            module_search_path,
            args.path_to_lib_in_xml
        )
    else:
        index_single(
            args.db_path,
            args.db_table,
            args.index_path,
            module_search_path,
            args.path_to_lib_in_xml
        )
