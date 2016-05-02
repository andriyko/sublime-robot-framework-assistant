import sublime_plugin
import sublime


class LogCommands(sublime_plugin.TextCommand):

    def run(self, edit):
        """Enables the default Sublime feature log_commands.

        For more details, see the Sublime API document:
        https://www.sublimetext.com/docs/3/api_reference.html
        """
        sublime.log_commands(True)
