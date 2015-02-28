import sublime
import sublime_plugin

# Plugin imports
try:
    from rfassistant import PY2
except ImportError:
    from ...rfassistant import PY2

if PY2:
    from rfassistant.rflint.rflint_git import RflintUtils
else:
    from ...rfassistant.rflint.rflint_git import RflintUtils


class RobotFrameworkRflintOpenTabCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()
        result = self._run_fr_lint(file_name)
        curr_view = self.view.window().new_file()
        if result:
            self._log_result(edit, curr_view, result)
        else:
            curr_view.insert(edit, 0, 'No file open or wrong type of file')

    def _run_fr_lint(self, file_name):
        rflint = RflintUtils()
        return rflint.run_fr_lint(file_name)

    def _log_result(self, edit, curr_view, result):
        rflint = RflintUtils()
        rflint.log_to_tab(edit, curr_view, result)
