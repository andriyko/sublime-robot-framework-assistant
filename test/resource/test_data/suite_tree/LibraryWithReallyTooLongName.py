from robot.api.deco import keyword
from robot.api import logger


class LibraryWithReallyTooLongName(object):

    @keyword
    def long_name_keyword(self, *args):
        """Documentation goes here"""
        logger.info(args)

    def other_long_name_keyword(self, *args, **kwargs):
        """Other documentation goes here"""
        logger.info(args)
        logger.info(kwargs)

    @keyword(name='Other Name Here')
    def not_name(self, arg):
        """def not_name kw name Other Name Here"""
        logger.info(arg)

    @keyword(name='Other ${arg1} and ${arg2} Too')
    def keyword_deco(self, arg1, arg2):
        """lib keyword with emmedded args"""
        logger.info(arg1)
        logger.info(arg2)
