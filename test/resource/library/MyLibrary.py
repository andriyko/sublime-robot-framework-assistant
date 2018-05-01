from robot.api import logger


class MyLibrary(object):

    def keyword_1(self, arg1):
        """kw 1 doc
        Tags: tag1, tag2
        """
        logger.info(arg1)

    def keyword_2(self, arg2, arg3):
        """kw 2 doc"""
        logger.info(arg2)
        logger.info(arg3)
