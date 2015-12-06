import shutil
from os import path, makedirs
from robot.errors import DataError
from finder import finder
from dataparser.parser.TestDataParser import TestDataParser
from queue import ParsingQueue


class Scanner(object):
    """Class to perform initial scanning of robot data.

    Creates initial database of keywords and variables. The class should
    be used when files are changed without saving them from Sublime. Example
    when files are changed by version control, like with git pull command.

    The database is folder where robot data is saved as json files.
    """
    def __init__(self):
        self.queue = ParsingQueue()

    def scan(self, workspace, ext, db_path):
        """Scan and create the database

        ``workspace`` --root folder where robot data is scanned.
        ``ext`` --Extension for included files.
        ``db_path`` --Directory where files are saved"""
        if not path.exists(workspace):
            raise EnvironmentError(
                'Workspace does not exist: {0}'.format(str(workspace)))
        if not path.dirname(workspace):
            raise EnvironmentError(
                'Workspace must be folder: {0}'.format(str(workspace)))
        if not path.exists(db_path):
            makedirs(db_path)
        else:
            shutil.rmtree(db_path)
        for f in finder(workspace, ext):
            self.queue.add(f, None)
        # Some sort of while loop
        # to read items from queue, scan and save to db_path

    def scan_resource(self, f):
        try:
            return TestDataParser().parse_resource(f)
        except DataError:
            return {}

    def scan_suite(self, f):
        try:
            return TestDataParser().parse_suite(f)
        except DataError:
            return {}
