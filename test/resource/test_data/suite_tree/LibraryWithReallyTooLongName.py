from robot.api.deco import keyword


class LibraryWithReallyTooLongName(object):

    def long_name_keyword(self, *args):
        """Documentation goes here"""
        print args

    def other_long_name_keyword(self, *args, **kwargs):
        """Other documentation goes here"""
        print args, kwargs

    @keyword(name='Other Name Here')
    def not_name(self, arg):
        """def not_name kw name Other Name Here"""
        print arg

    @keyword(name='Other ${arg1} and ${arg2} Too')
    def keyword_deco(self, arg1, arg2):
        """lib keyword with emmedded args"""
        print arg1, arg2
