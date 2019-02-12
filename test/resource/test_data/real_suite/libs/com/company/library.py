from robot.libraries.BuiltIn import BuiltIn


class CompanyLibrary(object):
    """docstring for ComparyLibrary"""

    def company_keyword(self, arg):
        print arg

    def company_keyword_2(self, args):
        print args
        print BuiltIn().get_library_instance('Selenium2Library')
