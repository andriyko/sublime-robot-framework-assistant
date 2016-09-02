import sublime_plugin
import sublime


class ScanAndIndexOpenTab(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.run_command('scan_open_tab')
        self.view.run_command('index_open_tab')
