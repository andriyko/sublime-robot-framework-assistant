from robot.api.deco import keyword


class LibraryNameWhichIsLongerThan100CharactersButItSeemsThatItRequiresQuiteAlotLettersInTheFileNameAndIsNotGoodRealLifeExample(object):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    @keyword(name='Keyword Which Also Has Really Long Name But Not As Long The Class Name By ${argument} In Keyword')
    def function(self, argument):
        """Documentation is here"""
        print argument
