import sublime
import sublime_plugin
from subprocess import Popen
from subprocess import PIPE
from os.path import join
from os.path import isfile

try:
    from rfassistant import PY2
except ImportError:
    from ...rfassistant import PY2

if PY2:
    from rfassistant import rflint_setting_filename
else:
    from ...rfassistant import rflint_setting_filename


class RobotFrameworkRflintGitStagedChangedFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        git = RflintGitSupport()
        rflint = RflintUtils()
        git_repo = rflint.get_git_repo()
        files = git.get_staged_files(git_repo)
        files += git.get_changed_files(git_repo)
        curr_view = self.view.window().new_file()
        for git_file in reversed(files):
            git_file = git_file.decode('utf-8')
            result = rflint.run_fr_lint(join(git_repo, git_file))
            rflint.log_to_tab(edit, curr_view, result)


class RobotFrameworkRflintGitStagedChangedUntrackedFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        git = RflintGitSupport()
        rflint = RflintUtils()
        git_repo = rflint.get_git_repo()
        files = git.get_staged_files(git_repo)
        files += git.get_changed_files(git_repo)
        files += git.get_untracked_files(git_repo)
        curr_view = self.view.window().new_file()
        curr_view.insert(edit, 0, git_repo)
        for git_file in reversed(files):
            git_file = git_file.decode('utf-8')
            result = rflint.run_fr_lint(join(git_repo, git_file))
            rflint.log_to_tab(edit, curr_view, result)


class RflintUtils():
    def log_to_tab(self, edit, curr_view, results):
        if results:
            for line in reversed(results):
                line = line.decode('utf-8') + '\n'
                curr_view.insert(edit, 0, line)
        else:
            curr_view.insert(edit, 0, 'Not valid results\n' + str(results))

    def run_fr_lint(self, file_name):
        if file_name is None:
            return False
        elif isfile(file_name):
            proc = Popen(['rflint', file_name],
                         shell=True,
                         stdout=PIPE)
            return proc.communicate()[0].splitlines()
        else:
            return False

    def get_git_repo(self):
        settings = sublime.load_settings(rflint_setting_filename)
        return settings.get('git_repo')


class RflintGitSupport():
    def get_changed_files(self, git_dir):
        proc = Popen(['git', 'diff', '--name-only'],
                     shell=True,
                     cwd=git_dir,
                     stdout=PIPE)
        return self._wait_and_return_files(proc)

    def get_staged_files(self, git_dir):
        proc = Popen(['git', 'diff', '--name-only', '--cached'],
                     shell=True,
                     cwd=git_dir,
                     stdout=PIPE)
        return self._wait_and_return_files(proc)

    def get_untracked_files(self, git_dir):
        proc = Popen(['git', 'ls-files', '--others', '--exclude-standard'],
                     shell=True,
                     cwd=git_dir,
                     stdout=PIPE)
        return self._wait_and_return_files(proc)

    def _wait_and_return_files(self, proc):
        proc.wait()
        return proc.stdout.read().splitlines()
