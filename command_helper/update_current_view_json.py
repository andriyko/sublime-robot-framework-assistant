from ..setting.setting import get_setting
from ..setting.setting import SettingObject
from ..command_helper.current_view import CurrentView


def update_current_view_index(view):
    file_name = view.file_name()
    message = None
    if file_name:
        cv = CurrentView()
        workspace = get_setting(SettingObject.workspace)
        index_dir = get_setting(SettingObject.index_dir)
        extension = get_setting(SettingObject.extension)
        if cv.view_in_db(workspace, file_name, index_dir, extension):
            view_path = get_setting(SettingObject.view_path)
            cv.create_view(file_name, view_path, index_dir)
            message = 'Updating index is done for file: {0} '.format(
                file_name
            )
            print(message)
    return message
