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
