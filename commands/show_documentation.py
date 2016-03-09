import sublime_plugin
import sublime
from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..command_helper.current_view import CurrentView
from ..command_helper.utils.get_text import get_line
from ..command_helper.noralize_cell import ReturnKeywordAndObject
from ..command_helper.get_metadata import get_rf_table_separator
from ..command_helper.get_documentation import GetKeywordDocumentation


class ShowKeywordDocumentation(sublime_plugin.TextCommand):

    def run(self, edit):
        w = sublime.active_window()
        panel = w.create_output_panel('kw_documentation')
        current_view = CurrentView()
        workspace = get_setting(SettingObject.workspace)
        open_tab = self.view.file_name()
        index_db = get_setting(SettingObject.index_dir)
        rf_extension = get_setting(SettingObject.extension)
        view_in_db = current_view.view_in_db(workspace, open_tab,
                                             index_db, rf_extension)
        db_dir = get_setting(SettingObject.table_dir)
        rf_cell = get_rf_table_separator(self.view)
        view_completions = get_setting(
            SettingObject.view_completions)
        if view_in_db:
            line, column = get_line(self.view)
            get_kw = ReturnKeywordAndObject(
                view_completions,
                rf_cell,
                rf_extension
            )
            keyword, object_name = get_kw.normalize(line, column)
            get_doc = GetKeywordDocumentation(
                db_dir,
                index_db,
                open_tab,
                rf_extension
            )
            doc = get_doc.return_documentation(object_name, keyword)
            if not doc:
                doc = 'No documentation found for keyword: "{0}"'.format(
                    keyword)
            panel.run_command('append', {'characters': doc})
            w.run_command('show_panel', {'panel': 'output.kw_documentation'})
