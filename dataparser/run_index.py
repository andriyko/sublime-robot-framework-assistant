import argparse
import sys
from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
SETTING_DIR = path.join(ROOT_DIR, '..', 'setting')
sys.path.append(SETTING_DIR)

from index.index import Index


def index_all(db_path, index_path):
    index = Index()
    index.index_all_tables(
        db_path=db_path,
        index_path=index_path
    )

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
        '--index_path',
        required=True,
        help='Folder where index result is saved'
    )
    args = c_parser.parse_args()
    if args.mode == 'all':
        index_all(args.db_path, args.index_path)
    else:
        """To index single file"""
        raise ValueError('Not implemented')
